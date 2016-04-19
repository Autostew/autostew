from time import sleep

from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionState
from autostew_web_session.models.event import Event


class HandleSessionStart(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.state_changed and
            event.new_session_state == SessionState.lobby and
            server.current_session is None
        ) or (
            event.type.name == EventType.session_created
        )

    @classmethod
    def consume(cls, server, event: Event):
        sleep(3)
        server.back_start_session()
