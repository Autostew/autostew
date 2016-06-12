from _thread import start_new_thread

import time

from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType
from autostew_web_session.models.event import Event

welcome_message = [
    "",
    "Welcome {player_name}, current setup is {setup_name}",
    "{safety_class_message}",
    "{elo_rating_message}",
    "See more information at autostew.net",
    "THIS IS AN OPEN ALPHA RELEASE OF AUTOSTEW",
    "{custom_motd}",
    "",
]


class HandleNotificationWelcome(BaseEventHandler):

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
        safety_class_message = cls.get_safety_class_message(steam_user)
        rating_message = cls.get_performance_rating_message(steam_user)

        if server.back_minimal_safety_class:
            steam_user.update_safety_class()
            if steam_user.safety_class.order > server.back_minimal_safety_class.order:
                event.member.send_chat('You will be kicked in 10 seconds because your safety class is too high!', server)
                start_new_thread(server.kick, (server, event.member.ref_id, 10))
        else:
            for message in welcome_message:
                event.member.send_chat(
                    message.format(
                        setup_name=server.current_session.setup_actual.name,
                        player_name=event.member.name,
                        safety_class_message=safety_class_message,
                        elo_rating_message=rating_message,
                        custom_motd=server.back_custom_motd
                    ), server
                )

    @classmethod
    def wait_and_kick(cls, server, ref_id, sleep_seconds):
        time.sleep(sleep_seconds)
        server.kick(ref_id)

    @classmethod
    def get_performance_rating_message(cls, steam_user):
        if not steam_user.elo_rating:
            rating_message = "You are currently unrated"
        else:
            rating_message = "Your current performance rating is {}".format(steam_user.elo_rating)
        return rating_message

    @classmethod
    def get_safety_class_message(cls, steam_user):
        if not steam_user.safety_class:
            safety_class_message = "You will be assigned a safety class"
        elif steam_user.safety_class.kick_on_impact_threshold:
            safety_class_message = "Your current safety class is {}. Drive carefully or you will be kicked!".format(
                steam_user.safety_class.name
            )
        else:
            safety_class_message = "Your current safety class is {}.".format(
                steam_user.safety_class.name
            )
        return safety_class_message
