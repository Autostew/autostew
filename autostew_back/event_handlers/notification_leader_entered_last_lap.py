from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionStage
from autostew_web_session.models.event import Event

leader_in_last_lap = [
    "",
    "The leader {leader_name} just entered their last lap!"
]


class HandleNotificationLeaderEnteredLastLap(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.participant is not None and
            event.type.name == EventType.lap and
            event.lap == server.current_session.setup_actual.race1_length - 2 and
            event.race_position == 1 and
            server.current_session.session_stage.name == SessionStage.race1 and
            not server.current_session.setup_actual.timed_race
        )

    @classmethod
    def consume(cls, server, event: Event):
        for message in leader_in_last_lap:
            server.send_chat(message.format(leader_name=event.participant.name))
