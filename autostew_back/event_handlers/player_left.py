from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_back.utils import td_to_milli
from autostew_web_enums.models import EventType, SessionStage
from autostew_web_session.models.event import Event
from autostew_web_session.models.models import RaceLapSnapshot, Lap, Sector


class HandlePlayerLeft(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.PlayerLeft and
            event.member is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        event.member.leaving_reason = event.leaving_reason
        event.member.save()
