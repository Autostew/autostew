from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_back.utils import td_to_milli
from autostew_web_enums.models import EventType, SessionStage
from autostew_web_session.models.event import Event
from autostew_web_session.models.models import RaceLapSnapshot, Lap, Sector


class HandleResult(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.results and
            event.participant is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        if not server.current_session.is_result:
            server.current_session.is_result = True
            server.current_session.save()
        if server.current_session.session_stage.name == SessionStage.race1:
            server.current_session.is_final_result = True
            server.current_session.save()
            event.participant.has_final_result = True
        event.participant.fastest_lap_time = td_to_milli(event.fastest_lap_time)
        event.participant.lap = event.lap
        event.participant.state = event.participant_state
        event.participant.race_position = event.race_position
        event.participant.total_time = td_to_milli(event.total_time)
        event.participant.save()

        if not server.current_session.participant_set.filter(has_final_result=False).exists():
            server.back_close_session()
