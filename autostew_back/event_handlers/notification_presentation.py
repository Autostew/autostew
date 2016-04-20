from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType
from autostew_web_session.models.event import Event

message = [
    "{name}: {safety} / {elo}",
]


class HandleNotificationPresentation(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.authenticated and
            event.member is not None and
            event.member.steam_user is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        steam_user = event.member.steam_user

        for m in message:
            server.send_chat(
                m.format(
                    name=steam_user.display_name,
                    safety=steam_user.safety_class.name if steam_user.safety_class is not None else "Unrated",
                    elo=steam_user.elo_rating,
                )
            )
