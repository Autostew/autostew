from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionState
from autostew_web_session.models.event import Event

new_session_starts = [
    "",
    "This server is connected to autostew.net"
    "",
]


class HandleNotificationNewSessionStart(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.state_changed and
            event.new_session_state is not None and
            event.new_session_state.name == SessionState.lobby
        )

    @classmethod
    def consume(cls, server, event: Event):
        for message in new_session_starts:
            server.send_chat(message)
