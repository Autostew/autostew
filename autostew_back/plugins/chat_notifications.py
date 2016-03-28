"""
Show a message when a player logs in (and other messages, too)
"""
from autostew_back.gameserver.event import EventType, BaseEvent, LapEvent, MemberEvent
from autostew_back.gameserver.server import Server
from autostew_back.gameserver.session import SessionStage, SessionState, SessionFlags

name = 'motd'

welcome_message = [
    "Welcome {player_name}, current setup is {setup_name}",
]
new_session_starts = [
    "This server is connected to autostew.selfhost.eu"
]
race_starts = [
    " ### RACE IS STARTING ###",
    "Keep the race safe and fair! Good luck!",
    "Be EXTRA CAREFUL on the first turn.",
    "Remind that players who crash too much will be kicked.",
]
leader_in_last_lap = [
    "The leader {leader_name} just entered their last lap!"
]
first_player_finished = [
    "Congratulations to {winner_name} for winning this race!",
    "See this race results and more at autostew.selfhost.eu"
]


def event(server: Server, event:BaseEvent):

    if event.type == EventType.authenticated:
        send_welcome_message(event, server)

    if (
        event.type == EventType.lap and
        event.lap == server.session.race1_length.get() - 1 and
        event.race_position == 1 and
        server.session.session_stage.get() == SessionStage.race1 and
        SessionFlags.timed_race not in server.session.flags.get_flags()
    ):
        send_winner_message(event, server)

    if (
        event.type == EventType.lap and
        event.lap == server.session.race1_length.get() - 2 and
        event.race_position == 1 and
        server.session.session_stage.get() == SessionStage.race1 and
        SessionFlags.timed_race not in server.session.flags.get_flags()
    ):
        send_winner_message(event, server)

    if event.type == EventType.state_changed and event.new_state == SessionState.lobby:
        send_new_session_message(server)

    if event.type == EventType.stage_changed and event.new_stage == SessionStage.race1:
        send_race_start_message(server)


def send_race_start_message(server: Server):
    for message in race_starts:
        server.api.send_chat(message)


def send_new_session_message(server: Server):
    for message in new_session_starts:
        server.api.send_chat(message)


def send_leader_in_last_lap_message(event: LapEvent, server: Server):
    for message in first_player_finished:
        server.api.send_chat(message.format(winner_name=event.participant.name.get()))


def send_winner_message(event: LapEvent, server: Server):
    for message in leader_in_last_lap:
        server.api.send_chat(message.format(leader_name=event.participant.name.get()))


def send_welcome_message(event: MemberEvent, server: Server):
    for message in welcome_message:
        event.member.send_chat(
            message.format(
                setup_name=server.get_current_setup_name(),
                player_name=event.member.name.get()
            )
        )
