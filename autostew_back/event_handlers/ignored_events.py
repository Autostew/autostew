from datetime import timedelta

from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_back.utils import td_to_milli, std_time_format
from autostew_web_enums.models import EventType, SessionStage
from autostew_web_session.models.event import Event
from autostew_web_session.models.models import RaceLapSnapshot, Lap
from autostew_web_session.models.session import Session


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