from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionStage
from autostew_web_session.models.event import Event

race_starts = [
    "",
    "",
    " ### RACE IS STARTING ###",
    "Keep the race safe and fair! Good luck!",
    "Be EXTRA CAREFUL on the first turn.",
]

warn_kicks_active = "Remind that players who crash too much will be kicked."


class HandleNotificationRaceStart(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.stage_changed and
            event.new_session_stage is not None and
            event.new_session_stage.name == SessionStage.race1
        )

    @classmethod
    def consume(cls, server, event: Event):
        for message in race_starts:
            server.send_chat(message)

        if server.back_kicks:
            server.send_chat(warn_kicks_active)
