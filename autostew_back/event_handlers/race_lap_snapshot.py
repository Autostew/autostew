from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionStage, SessionState
from autostew_web_session.models.event import Event
from autostew_web_session.models.models import RaceLapSnapshot


class HandleRaceLapSnapshot(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.lap and
            event.race_position == 1 and
            server.current_session is not None and
            server.current_session.session_stage is not None and
            server.current_session.session_stage.name == SessionStage.race1
        )

    @classmethod
    def consume(cls, server, event: Event):
        snapshot = server.current_session.create_snapshot()
        RaceLapSnapshot.objects.create(lap=event.lap + 1, snapshot=snapshot, session=server.current_session)
