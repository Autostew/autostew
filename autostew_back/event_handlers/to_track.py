from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionState
from autostew_web_session.models.event import Event


class HandleToTrack(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.state_changed and
            event.new_session_state == SessionState.race and
            server.current_session is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        actual_setup = server.back_pull_session_setup()
        actual_setup.name = server.current_session.setup_template.name
        server.current_session.setup_actual = actual_setup
        server.current_session.create_snapshot()
