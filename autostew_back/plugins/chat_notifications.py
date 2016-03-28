"""
Show a message when a player logs in (and other messages, too)
"""
from autostew_back.gameserver.event import EventType, BaseEvent
from autostew_back.gameserver.server import Server
from autostew_back.gameserver.session import SessionStage, SessionState

name = 'motd'

welcome_message = [
    "Welcome",
    "Current setup is {setup_name}",
]
first_player_finished = [
    "Congratulations to {winner_name} for winning this race!",
    "See this race results and more about Autostew at autostew.selfhost.eu"
]
new_session_starts = [
    "The next session is starting",
    "See the session's results and more at autostew.selfhost.eu"
]


def event(server: Server, event:BaseEvent):

    if event.type == EventType.authenticated:
        for message in welcome_message:
            event.member.send_chat(message.format(setup_name=server.get_current_setup_name()))

    if event.type == EventType.results and event.race_position == 1 and server.session.session_stage == SessionStage.race1:
        for message in first_player_finished:
            server.api.send_chat(message.format(winner_name=event.participant.name.get()))

    if event.type == EventType.state_changed and event.new_state == SessionState.lobby:
        for message in new_session_starts:
            server.api.send_chat(message)
