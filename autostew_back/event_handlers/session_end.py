from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionState
from autostew_web_session.models.event import Event
from autostew_web_session.models.member import Member
from autostew_web_session.models.session import Session


class HandleSessionEnd(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.state_changed and
            event.new_session_state == SessionState.lobby and
            server.current_session is not None
        ) or (
            event.type.name == EventType.session_destroyed and
            server.current_session is not None
        ) or (
            event.type.name == EventType.state_changed and
            event.new_session_state == SessionState.post_race and
            server.current_session.is_final_result
        )

    @classmethod
    def consume(cls, server, event: Event):
        server.back_close_session()