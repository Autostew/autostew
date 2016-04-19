from datetime import timedelta

from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_back.utils import td_to_milli, std_time_format
from autostew_web_enums.models import EventType, SessionStage
from autostew_web_session.models.event import Event
from autostew_web_session.models.models import RaceLapSnapshot, Lap
from autostew_web_session.models.session import Session


class HandleLap(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.lap and
            event.participant is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        new_lap = Lap.objects.create(
            session=server.current_session,
            session_stage=server.current_session.session_stage,
            participant=event.participant,
            lap=event.lap + 1,
            count_this_lap=event.count_this_lap_times,
            lap_time=td_to_milli(event.lap_time),
            position=event.race_position,
            sector1_time=td_to_milli(event.sector1_time),
            sector2_time=td_to_milli(event.sector2_time),
            sector3_time=td_to_milli(event.sector3_time),
            distance_travelled=event.distance_travelled,
        )

        if event.participant.is_player and event.member:
            event.member.steam_user.add_distance(event.distance_travelled)

        if not server.current_session.session_stage.name.startswith("Race"):
            server.current_session.reorder_by_best_time()

        if cls.is_new_fastest_lap(new_lap, server.current_session):
            cls.announce_lap(new_lap, server)

    @classmethod
    def is_new_fastest_lap(cls, lap: Lap, session: Session):
        if not lap.count_this_lap:
            return False
        if session.fastest_lap is None or lap.lap_time < session.fastest_lap.lap_time:
            session.fastest_lap = lap
            session.save()
            return True
        return False

    @classmethod
    def announce_lap(cls, lap: Lap, server):
        message = "FASTEST LAP: P{position} - {participant} - {laptime}".format(
            participant=lap.participant.name,
            laptime=std_time_format(timedelta(milliseconds=lap.lap_time)),
            position=lap.participant.race_position,
        )
        server.send_chat("")
        server.send_chat(message)
