"""
Show a message when a player logs in (and other messages, too)
"""
from autostew_back.gameserver.event import EventType, BaseEvent, LapEvent, MemberEvent
from autostew_web_session.models.server import Server
from autostew_web_users.models import SteamUser

name = 'chat_notifications'

race_starts = [
    "",
    "",
    " ### RACE IS STARTING ###",
    "Keep the race safe and fair! Good luck!",
    "Be EXTRA CAREFUL on the first turn.",
    "Remind that players who crash too much will be kicked.",
]


def event(server: Server, event: BaseEvent):

    if event.type == EventType.stage_changed and event.new_stage == SessionStage.race1:
        send_race_start_message(server)


def send_race_start_message(server: Server):
    for message in race_starts:
        server.api.send_chat(message)


def send_new_session_message(server: Server):
    for message in new_session_starts:
        server.api.send_chat(message)


def send_leader_in_last_lap_message(event: LapEvent, server: Server):
    if event.participant:
        for message in leader_in_last_lap:
            server.api.send_chat(message.format(leader_name=event.participant.name.get()))


def send_winner_message(event: LapEvent, server: Server):
    if event.participant:
        for message in first_player_finished:
            server.api.send_chat(message.format(winner_name=event.participant.name.get()))


def send_welcome_message(event: MemberEvent, server: Server):
    if not event.member:
        return
    try:
        steam_user = SteamUser.objects.get(steam_id=event.member.steam_id.get())
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

        if not steam_user.elo_rating:
            rating_message = "You are currently unrated"
        else:
            rating_message = "Your current rating is {}".format(steam_user.elo_rating)

        for message in welcome_message:
            event.member.send_chat(
                message.format(
                    setup_name=server.get_current_setup_name(),
                    player_name=event.member.name.get(),
                    safety_class_message=safety_class_message,
                    elo_rating_message=rating_message
                )
            )
    except SteamUser.DoesNotExist:
        pass
