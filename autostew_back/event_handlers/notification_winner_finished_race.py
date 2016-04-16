from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionStage
from autostew_web_session.models.event import Event

first_player_finished = [
    "",
    "",
    "Congratulations to {winner_name} for winning this race!",
    "See this race results and more at autostew.net"
]


class HandleNotificationWinnerFinishedRace(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.participant is not None and
            event.type.name == EventType.lap and
            event.lap == server.current_session.setup_actual.race1_length - 1 and
            event.race_position == 1 and
            server.current_session.session_stage.name == SessionStage.race1 and
            not server.current_session.setup_actual.timed_race
        )

    @classmethod
    def consume(cls, server, event: Event):
        for message in first_player_finished:
            server.send_chat(message.format(winner_name=event.participant.name))
