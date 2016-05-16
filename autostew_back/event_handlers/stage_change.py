from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionState
from autostew_web_session.models.event import Event


class HandleStageChange(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.stage_changed and
            server.current_session is not None and
            server.current_session.session_state not in (SessionState.returning, SessionState.lobby)
        )

    @classmethod
    def consume(cls, server, event: Event):
        server.current_session.create_snapshot()
        server.current_session.is_result = False
        server.current_session.fastest_lap_time = None
        server.current_session.session_stage = event.new_session_stage
        server.current_session.save()
