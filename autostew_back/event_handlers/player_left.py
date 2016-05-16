from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType
from autostew_web_session.models.event import Event


class HandlePlayerLeft(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.player_left and
            event.member is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        event.member.leaving_reason = event.leaving_reason
        event.member.save()
