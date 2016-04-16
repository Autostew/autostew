import json
import logging

from django.db import transaction
from django.utils import timezone

import autostew_web_session.models.event
import autostew_web_session.models.member
import autostew_web_session.models.participant
import autostew_web_session.models.server
import autostew_web_session.models.session
from autostew_back.gameserver.event import EventType, BaseEvent, ParticipantEvent
from autostew_back.gameserver.member import Member as SessionMember
from autostew_back.gameserver.participant import Participant as SessionParticipant
from autostew_back.plugins import db, db_setup_rotation
from autostew_back.plugins.db_session_writer_libs import db_elo_rating, db_safety_rating
from autostew_back.utils import td_to_milli
from autostew_web_enums import models as enum_models
from autostew_web_session.models import models as session_models
from autostew_web_session.models.server import Server
from autostew_web_users.models import SteamUser



@transaction.atomic
def destroy(server: Server):
    global current_session
    if current_session:
        current_session.running = False
        current_session.save()
        current_session = None


@transaction.atomic
def event(server: Server, event: (BaseEvent, ParticipantEvent)):
    global current_session

    # Creates snapshot and RaceLapSnapshot on each lap in the race by the leader
    if event.type == EventType.lap and event.race_position == 1 and server.session_api.session_stage.get_nice() == SessionStage.race1:
        snapshot = _create_session_snapshot(server, current_session)
        session_models.RaceLapSnapshot(lap=event.lap + 1, snapshot=snapshot, session=current_session).save()

    # Stores each lap
    if event.type == EventType.lap:
        participant = _get_or_create_participant(current_session, event.participant)
        session_models.Lap(
            session=current_session,
            session_stage=enum_models.SessionStage.objects.get(name=server.session_api.session_stage.get()),
            participant=participant,
            lap=event.lap + 1,
            count_this_lap=event.count_this_lap_times,
            lap_time=td_to_milli(event.lap_time),
            position=event.race_position,
            sector1_time=td_to_milli(event.sector1_time),
            sector2_time=td_to_milli(event.sector2_time),
            sector3_time=td_to_milli(event.sector3_time),
            distance_travelled=event.distance_travelled,
        ).save()

        if event.count_this_lap_times and not participant.is_ai:
            db_safety_rating.lap_completed(participant.member.steam_user)

        if not current_session.current_snapshot.session_stage.name.startswith("Race"):
            _get_or_create_participant_snapshot(
                event.participant,
                current_session,
                current_session.current_snapshot,
                overwrite=True
            )
            current_session.current_snapshot.reorder_by_best_time()

    # Stores each sector
    if event.type == EventType.sector and event.lap > 0:
        session_models.Sector(
            session=current_session,
            session_stage=enum_models.SessionStage.objects.get(name=server.session_api.session_stage.get()),
            participant=autostew_web_session.models.participant.Participant.objects.get(ingame_id=event.participant.id.get(),
                                                                                        refid=event.participant.refid.get(),
                                                                                        session=current_session),
            lap=event.lap,
            count_this_lap=event.count_this_lap,
            sector=event.sector,
            sector_time=td_to_milli(event.sector_time),
        ).save()

    # Writes results as a new snapshot
    if event.type == EventType.results and event.participant:
        try:
            result_snapshot = autostew_web_session.models.session.SessionSnapshot.objects.get(
                session=current_session,
                is_result=True,
                session_stage__name=server.session_api.session_stage.get()
            )
        except autostew_web_session.models.session.SessionSnapshot.DoesNotExist:
            result_snapshot = _create_session_snapshot(server, current_session)
            result_snapshot.is_result = True
            result_snapshot.save()

        participant = autostew_web_session.models.participant.ParticipantSnapshot.objects.get(
            snapshot=result_snapshot,
            participant__ingame_id=event.participant_id
        )
        participant.fastest_lap_time = td_to_milli(event.fastest_lap_time)
        participant.lap = event.lap
        participant.state = enum_models.ParticipantState.objects.get(name=event.state.value)
        participant.race_position = event.race_position
        participant.total_time = td_to_milli(event.total_time)
        participant.save()
        current_stage = _get_or_create_stage(server, server.session_api.session_stage.get())
        current_stage.result_snapshot = result_snapshot
        current_stage.save()

    # Creates or updates participant
    # Creating the participants when the session starts is not enough, as at that point not all information may be there
    if event.type == EventType.participant_created and event.participant:
        participant = _get_or_create_participant(current_session, event.participant)
        participant.name = event.name
        participant.is_ai = not event.is_player
        participant.vehicle = session_models.Vehicle.objects.get(ingame_id=event.vehicle)
        participant.livery = session_models.Livery.objects.get(id_for_vehicle=event.livery,
                                                               vehicle__ingame_id=event.vehicle)
        participant.save()

    # Destroy a participant
    if event.type == EventType.participant_destroyed:
        participant = autostew_web_session.models.participant.Participant.objects.get(ingame_id=event.raw['participantid'],
                                                                                      session=current_session)
        participant.still_connected = False
        participant.save()

    # Creates a member
    if event.type == EventType.authenticated:
        if current_session is not None and event.member is not None:
            _get_or_create_member(current_session, event.member)

    # Destroys a member
    if event.type == EventType.player_left:
        try:
            member = autostew_web_session.models.member.Member.objects.get(refid=event.refid, session=current_session)
            member.still_connected = False
            member.save()
        except autostew_web_session.models.member.Member.DoesNotExist:
            pass

    # Destroys the session
    if event.type == EventType.session_destroyed:
        _close_current_session(server)

    # When session enters lobby, destroys current session if any and creates a new one.
    if event.type == EventType.state_changed and event.new_session_state == SessionState.lobby:
            if current_session is not None:
                _close_current_session(server)
            current_session = _get_or_create_session(server)

    # When session enters track, makes snapshot
    if event.type == EventType.state_changed and event.new_session_state == SessionState.race:
            final_setup = _create_session_setup(server)
            final_setup.id = current_session.setup_actual_id
            final_setup.save(force_update=True)
            current_session.starting_snapshot_to_track = _create_session_snapshot(server, current_session)
            current_session.save()
            stage = _get_or_create_stage(server, server.session_api.session_stage.get())
            stage.starting_snapshot = current_session.starting_snapshot_to_track
            stage.save()

    # Create stage starting snapshots
    if event.type == EventType.stage_changed:
        if current_session.current_snapshot.session_state.name not in ("Returning", "Lobby"):
            snapshot = _create_session_snapshot(server, current_session)
            stage = _get_or_create_stage(server, event.new_session_stage.value)
            stage.starting_snapshot = snapshot
            stage.save()
            current_session.save()

    # Insert event
    # some events can happen while there is no session, we ignore them
    if current_session:
        autostew_web_session.models.event.Event(
            snapshot=None,
            definition=enum_models.EventDefinition.objects.get(name=event.type.value),
            session=current_session,
            timestamp=timezone.make_aware(event.time),
            ingame_index=event.index,
            raw=json.dumps(event.raw),
        ).save()


def _close_current_session(server:Server):
    global current_session
    if current_session:
        if current_session.current_snapshot.session_stage.is_relevant():
            current_session.finished = True
        current_session.running = False
        current_session.save()
        db_elo_rating.update_ratings_after_race_end(current_session)
    current_session = None
    server.current_session = None
    server.save()

