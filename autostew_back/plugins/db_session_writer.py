import json
import logging

from django.db import transaction
from django.utils import timezone

import autostew_web_session.models.member
import autostew_web_session.models.participant
import autostew_web_session.models.server
import autostew_web_session.models.session
from autostew_back.gameserver.event import EventType, BaseEvent, ParticipantEvent
from autostew_back.gameserver.member import MemberFlags, Member as SessionMember
from autostew_back.gameserver.participant import Participant as SessionParticipant
from autostew_web_session.models.server import ServerState
from autostew_back.gameserver.session import Privacy, SessionState, SessionStage
from autostew_web_session.models.session_enums import SessionFlags, SessionState, SessionStage, Privacy
from autostew_back.plugins import db, db_setup_rotation
from autostew_back.plugins.db_session_writer_libs import db_elo_rating, db_safety_rating
from autostew_back.utils import td_to_milli
from autostew_web_enums import models as enum_models
from autostew_web_session.models import models as session_models
from autostew_web_session.models.server import Server
from autostew_web_users.models import SteamUser

name = 'DB writer'
dependencies = [db, db_setup_rotation]

current_session = None


@transaction.atomic
def init(server: Server):
    global current_session
    if server.state == ServerState.running:
        current_session = _get_or_create_session(server)


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
    if event.type == EventType.state_changed and event.new_state == SessionState.lobby:
            if current_session is not None:
                _close_current_session(server)
            current_session = _get_or_create_session(server)

    # When session enters track, makes snapshot
    if event.type == EventType.state_changed and event.new_state == SessionState.race:
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
            stage = _get_or_create_stage(server, event.new_stage.value)
            stage.starting_snapshot = snapshot
            stage.save()
            current_session.save()

    # Insert event
    # some events can happen while there is no session, we ignore them
    if current_session:
        session_models.Event(
            snapshot=None,
            definition=enum_models.EventDefinition.objects.get(name=event.type.value),
            session=current_session,
            timestamp=timezone.make_aware(event.time),
            ingame_index=event.index,
            raw=json.dumps(event.raw),
        ).save()


def _get_or_create_stage(server: Server, new_stage: str):
    try:
        return autostew_web_session.models.session.SessionStage.objects.get(
            session=current_session,
            stage__name=new_stage
        )
    except autostew_web_session.models.session.SessionStage.DoesNotExist:
        stage = autostew_web_session.models.session.SessionStage(
            session=current_session,
            stage=enum_models.SessionStage.objects.get(name=new_stage)
        )
        stage.save()
        return stage


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


def _get_or_create_session(server: Server) -> autostew_web_session.models.session.Session:
    actual_setup = _create_session_setup(server)
    actual_setup.save()

    session = autostew_web_session.models.session.Session(
        server=server,
        setup_template=db_setup_rotation.current_setup.setup,
        setup_actual=actual_setup,
        lobby_id=server.lobby_id,
        max_member_count=server.max_member_count,
        running=True,
        finished=False,
    )

    if db_setup_rotation.scheduled_session:
        session.id = db_setup_rotation.scheduled_session.id
        session.planned = True
    else:
        session.planned = False
    session.save()

    for member in server.members_api.elements:
        _get_or_create_member(session, member)

    for participant in server.participants_api.elements:
        _get_or_create_participant(session, participant)

    snapshot = _create_session_snapshot(server, session)
    session.first_snapshot = snapshot
    session.save()
    server.current_session = session
    server.save()
    return session


def _create_session_setup(server):
    flags = server.session_api.flags.get_flags()
    return autostew_web_session.models.session.SessionSetup(
        name=db_setup_rotation.current_setup.setup.name,
        is_template=False,
        server_controls_setup=server.session_api.server_controls_setup.get(),
        server_controls_track=server.session_api.server_controls_track.get(),
        server_controls_vehicle_class=server.session_api.server_controls_vehicle_class.get(),
        server_controls_vehicle=server.session_api.server_controls_vehicle.get(),
        grid_size=server.session_api.grid_size.get(),
        max_players=server.session_api.max_players.get(),
        opponent_difficulty=server.session_api.opponent_difficulty.get(),
        force_identical_vehicles=SessionFlags.force_identical_vehicles in flags,
        allow_custom_vehicle_setup=SessionFlags.allow_custom_vehicle_setup in flags,
        force_realistic_driving_aids=SessionFlags.force_realistic_driving_aids in flags,
        abs_allowed=SessionFlags.abs_allowed in flags,
        sc_allowed=SessionFlags.sc_allowed in flags,
        tcs_allowed=SessionFlags.tcs_allowed in flags,
        force_manual=SessionFlags.force_manual in flags,
        rolling_starts=SessionFlags.rolling_starts in flags,
        force_same_vehicle_class=SessionFlags.force_same_vehicle_class in flags,
        fill_session_with_ai=SessionFlags.fill_session_with_ai in flags,
        mechanical_failures=SessionFlags.mechanical_failures in flags,
        auto_start_engine=SessionFlags.auto_start_engine in flags,
        timed_race=SessionFlags.timed_race in flags,
        ghost_griefers=SessionFlags.ghost_griefers in flags,
        enforced_pitstop=SessionFlags.enforced_pitstop in flags,
        practice1_length=server.session_api.practice1_length.get(),
        practice2_length=server.session_api.practice2_length.get(),
        qualify_length=server.session_api.qualify_length.get(),
        warmup_length=server.session_api.warmup_length.get(),
        race1_length=server.session_api.race1_length.get(),
        race2_length=server.session_api.race2_length.get(),
        public=server.session_api.privacy.get_nice() == Privacy.public,
        friends_can_join=server.session_api.privacy.get_nice() in (Privacy.public, Privacy.friends),
        damage=enum_models.DamageDefinition.objects.get(
            ingame_id=server.session_api.damage.get()) if server.session_api.damage.get() is not None else None,
        tire_wear=enum_models.TireWearDefinition.objects.get(
            ingame_id=server.session_api.tire_wear.get()) if server.session_api.tire_wear.get() is not None else None,
        fuel_usage=enum_models.FuelUsageDefinition.objects.get(
            ingame_id=server.session_api.fuel_usage.get()) if server.session_api.fuel_usage.get() is not None else None,
        penalties=enum_models.PenaltyDefinition.objects.get(
            ingame_id=server.session_api.penalties.get()) if server.session_api.penalties.get() is not None else None,
        allowed_views=enum_models.AllowedViewsDefinition.objects.get(
            ingame_id=server.session_api.allowed_views.get()) if server.session_api.allowed_views.get() is not None else None,
        track=session_models.Track.objects.get(
            ingame_id=server.session_api.track.get()) if server.session_api.track.get() is not None else None,
        vehicle_class=session_models.VehicleClass.objects.get(
            ingame_id=server.session_api.vehicle_class.get()) if server.session_api.vehicle_class.get() is not None else None,
        vehicle=session_models.Vehicle.objects.get(
            ingame_id=server.session_api.vehicle.get()) if server.session_api.vehicle.get() else None,
        date_year=server.session_api.date_year.get(),
        date_month=server.session_api.date_month.get(),
        date_day=server.session_api.date_day.get(),
        date_hour=server.session_api.date_hour.get(),
        date_minute=server.session_api.date_minute.get(),
        date_progression=server.session_api.date_progression.get(),
        weather_progression=server.session_api.weather_progression.get(),
        weather_slots=server.session_api.weather_slots.get(),
        weather_1=enum_models.WeatherDefinition.objects.get(
            ingame_id=server.session_api.weather_1.get()) if server.session_api.weather_1.get() else None,
        weather_2=enum_models.WeatherDefinition.objects.get(
            ingame_id=server.session_api.weather_2.get()) if server.session_api.weather_2.get() else None,
        weather_3=enum_models.WeatherDefinition.objects.get(
            ingame_id=server.session_api.weather_3.get()) if server.session_api.weather_3.get() else None,
        weather_4=enum_models.WeatherDefinition.objects.get(
            ingame_id=server.session_api.weather_4.get()) if server.session_api.weather_4.get() else None,
        game_mode=enum_models.GameModeDefinition.objects.get(
            ingame_id=server.session_api.game_mode.get()) if server.session_api.game_mode.get() else None,
        track_latitude=server.session_api.track_latitude.get(),
        track_longitude=server.session_api.track_longitude.get(),
        track_altitude=server.session_api.track_altitude.get(),
    )


def _get_or_create_steam_user(member: SessionMember) -> SteamUser:
    try:
        steam_user = SteamUser.objects.get(steam_id=member.steam_id.get())
        steam_user.display_name = member.name.get()
        steam_user.save()
    except SteamUser.DoesNotExist:
        steam_user = SteamUser(
            steam_id=member.steam_id.get(),
            display_name=member.name.get(),
            safety_rating=db_safety_rating.initial_safety_rating
        )
        steam_user.update_safety_class()
        steam_user.save()
    return steam_user


def _get_or_create_member(session: autostew_web_session.models.session.Session, member: SessionMember) -> autostew_web_session.models.member.Member:
    member_flags = member.race_stat_flags.get_flags()
    vehicle = session_models.Vehicle.objects.get(
        ingame_id=member.vehicle.get()) if member.vehicle.get() is not None else None
    steam_user = _get_or_create_steam_user(member)
    try:
        member_in_db = autostew_web_session.models.member.Member.objects.get(session=session, steam_id=member.steam_id.get())
    except autostew_web_session.models.member.Member.DoesNotExist:
        member_in_db = autostew_web_session.models.member.Member(session=session, steam_id=member.steam_id.get())
    member_in_db.steam_user = steam_user
    member_in_db.still_connected = True
    member_in_db.vehicle = vehicle
    member_in_db.livery = session_models.Livery.objects.get(id_for_vehicle=member.livery.get(),
                                                            vehicle=vehicle) if vehicle is not None else None
    member_in_db.refid = member.refid.get()
    member_in_db.name = member.name.get()
    member_in_db.setup_used = MemberFlags.setup_used in member_flags
    member_in_db.controller_gamepad = MemberFlags.controller_gamepad in member_flags
    member_in_db.controller_wheel = MemberFlags.controller_wheel in member_flags
    member_in_db.aid_steering = MemberFlags.aid_steering in member_flags
    member_in_db.aid_braking = MemberFlags.aid_braking in member_flags
    member_in_db.aid_abs = MemberFlags.aid_abs in member_flags
    member_in_db.aid_traction = MemberFlags.aid_traction in member_flags
    member_in_db.aid_stability = MemberFlags.aid_stability in member_flags
    member_in_db.aid_no_damage = MemberFlags.aid_no_damage in member_flags
    member_in_db.aid_auto_gears = MemberFlags.aid_auto_gears in member_flags
    member_in_db.aid_auto_clutch = MemberFlags.aid_auto_clutch in member_flags
    member_in_db.model_normal = MemberFlags.model_normal in member_flags
    member_in_db.model_experienced = MemberFlags.model_experienced in member_flags
    member_in_db.model_pro = MemberFlags.model_pro in member_flags
    member_in_db.model_elite = MemberFlags.model_elite in member_flags
    member_in_db.aid_driving_line = MemberFlags.aid_driving_line in member_flags
    member_in_db.valid = MemberFlags.valid in member_flags
    member_in_db.save()
    return member_in_db


def _get_or_create_participant(session: autostew_web_session.models.session.Session, participant: SessionParticipant) -> autostew_web_session.models.participant.Participant:
    member = autostew_web_session.models.member.Member.objects.get(refid=participant.refid.get(),
                                                                   session=session) if participant.is_player.get() else None
    try:
        participant = autostew_web_session.models.participant.Participant.objects.get(session=session, ingame_id=participant.id.get(),
                                                                                      member=member)
    except autostew_web_session.models.participant.Participant.DoesNotExist:
        vehicle = session_models.Vehicle.objects.get(
            ingame_id=participant.vehicle.get()) if participant.vehicle.get() is not None else None
        livery = session_models.Livery.objects.get(id_for_vehicle=participant.livery.get(),
                                                   vehicle=vehicle) if participant.livery.get() is not None else None
        participant = autostew_web_session.models.participant.Participant(
            member=member,
            session=session,
            still_connected=True,
            ingame_id=participant.id.get(),
            refid=participant.refid.get(),
            name=participant.name.get(),
            is_ai=not participant.is_player.get(),
            vehicle=vehicle,
            livery=livery,
        )
        participant.save()
    return participant


def _create_session_snapshot(server: Server, session: autostew_web_session.models.session.Session) -> autostew_web_session.models.session.SessionSnapshot:
    logging.info("Creating session snapshot")
    session_snapshot = autostew_web_session.models.session.SessionSnapshot(
        session=session,
        is_result=False,
        session_state=enum_models.SessionState.objects.get(
            name=server.session_api.session_state.get() if server.session_api.session_state.get() else None),
        session_stage=enum_models.SessionStage.objects.get(
            name=server.session_api.session_stage.get()) if server.session_api.session_stage.get() else None,
        session_phase=enum_models.SessionPhase.objects.get(
            name=server.session_api.session_phase.get()) if server.session_api.session_phase.get() else None,
        session_time_elapsed=server.session_api.session_time_elapsed.get(),
        session_time_duration=server.session_api.session_time_duration.get(),
        num_participants_valid=server.session_api.num_participants_valid.get(),
        num_participants_disq=server.session_api.num_participants_disq.get(),
        num_participants_retired=server.session_api.num_participants_retired.get(),
        num_participants_dnf=server.session_api.num_participants_dnf.get(),
        num_participants_finished=server.session_api.num_participants_finished.get(),
        current_year=server.session_api.current_year.get(),
        current_month=server.session_api.current_month.get(),
        current_day=server.session_api.current_day.get(),
        current_hour=server.session_api.current_hour.get(),
        current_minute=server.session_api.current_minute.get(),
        rain_density_visual=server.session_api.rain_density_visual.get(),
        wetness_path=server.session_api.wetness_path.get(),
        wetness_off_path=server.session_api.wetness_off_path.get(),
        wetness_avg=server.session_api.wetness_avg.get(),
        wetness_predicted_max=server.session_api.wetness_predicted_max.get(),
        wetness_max_level=server.session_api.wetness_max_level.get(),
        temperature_ambient=server.session_api.temperature_ambient.get(),
        temperature_track=server.session_api.temperature_track.get(),
        air_pressure=server.session_api.air_pressure.get(),
    )
    session_snapshot.save()

    for it in server.members_api.elements:
        _get_or_create_member(session, it)
        _create_member_snapshot(it, session, session_snapshot)

    for it in server.participants_api.elements:
        _get_or_create_participant(session, it)
        _get_or_create_participant_snapshot(it, session, session_snapshot)

    session.current_snapshot = session_snapshot
    session.save()
    return session_snapshot


def _get_or_create_participant_snapshot(
        participant: SessionParticipant,
        session: autostew_web_session.models.session.Session,
        session_snapshot: autostew_web_session.models.session.SessionSnapshot,
        overwrite=False
) -> autostew_web_session.models.participant.ParticipantSnapshot:
    participant_snapshot = None
    try:
        participant_snapshot = autostew_web_session.models.participant.ParticipantSnapshot.objects.get(
            snapshot=session_snapshot,
            participant__ingame_id=participant.id.get()
        )
        if not overwrite:
            return participant_snapshot
    except autostew_web_session.models.participant.ParticipantSnapshot.DoesNotExist:
        pass

    try:
        parent = autostew_web_session.models.participant.Participant.objects.get(ingame_id=participant.id.get(), session=session)
    except autostew_web_session.models.participant.Participant.DoesNotExist:
        parent = _get_or_create_participant(session, participant)

    if not participant_snapshot:
        participant_snapshot = autostew_web_session.models.participant.ParticipantSnapshot()

    participant_snapshot.snapshot = session_snapshot
    participant_snapshot.participant = parent
    participant_snapshot.still_connected = True
    participant_snapshot.grid_position = participant.grid_position.get()
    participant_snapshot.race_position = participant.race_position.get()
    participant_snapshot.current_lap = participant.current_lap.get()
    participant_snapshot.current_sector = participant.current_sector.get()
    participant_snapshot.sector1_time = participant.sector1_time.get()
    participant_snapshot.sector2_time = participant.sector2_time.get()
    participant_snapshot.sector3_time = participant.sector3_time.get()
    participant_snapshot.last_lap_time = participant.last_lap_time.get()
    participant_snapshot.fastest_lap_time = participant.fastest_lap_time.get()
    participant_snapshot.state = enum_models.ParticipantState.objects.get(name=participant.state.get())
    participant_snapshot.headlights = participant.headlights.get()
    participant_snapshot.wipers = participant.wipers.get()
    participant_snapshot.speed = participant.speed.get()
    participant_snapshot.gear = participant.gear.get()
    participant_snapshot.rpm = participant.rpm.get()
    participant_snapshot.position_x = participant.position_x.get()
    participant_snapshot.position_y = participant.position_y.get()
    participant_snapshot.position_z = participant.position_z.get()
    participant_snapshot.orientation = participant.orientation.get()
    participant_snapshot.total_time = 0
    participant_snapshot.save()
    return participant_snapshot


def _create_member_snapshot(
        member: SessionParticipant,
        session: autostew_web_session.models.session.Session,
        session_snapshot: autostew_web_session.models.session.SessionSnapshot
) -> autostew_web_session.models.member.MemberSnapshot:
    member_snapshot = autostew_web_session.models.member.MemberSnapshot(
        snapshot=session_snapshot,
        member=autostew_web_session.models.member.Member.objects.get(refid=member.refid.get(), session=session),
        still_connected=True,
        load_state=enum_models.MemberLoadState.objects.get_or_create(name=member.load_state.get())[0],
        ping=member.ping.get(),
        index=member.index.get(),
        state=enum_models.MemberState.objects.get(name=member.state.get()),
        join_time=member.join_time.get(),
        host=member.host.get(),
    )
    member_snapshot.save()
    return member_snapshot
