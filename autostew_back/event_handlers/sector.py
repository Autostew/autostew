from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_back.utils import td_to_milli
from autostew_web_enums.models import EventType, SessionStage
from autostew_web_session.models.event import Event
from autostew_web_session.models.models import RaceLapSnapshot, Lap, Sector


class HandleSector(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.sector and
            event.participant is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        Sector.objects.create(
            session=server.current_session,
            session_stage=server.current_session.session_stage,
            participant=event.participant,
            lap=event.lap,
            count_this_lap=event.count_this_lap,
            sector=event.sector,
            sector_time=td_to_milli(event.sector_time),
        )
