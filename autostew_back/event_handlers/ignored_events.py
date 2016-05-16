from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType
from autostew_web_session.models.event import Event


class HandleIgnore(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.participant_created or
            event.type.name == EventType.participant_destroyed or
            event.type.name == EventType.session_setup or
            event.type.name == EventType.participant_state or
            event.type.name == EventType.server_chat or
            event.type.name == EventType.player_chat or
            event.type.name == EventType.player_joined or
            event.type.name == EventType.player_left or
            event.type.name == EventType.cut_track_end or
            event.type.name == EventType.cut_track_start
        )

    @classmethod
    def consume(cls, server, event: Event):
        pass