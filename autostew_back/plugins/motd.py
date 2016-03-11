"""
Show a message when a player logs in.
"""
from autostew_back.gameserver.event import EventType

name = 'motd'

messages = [
    "Welcome",
    "Current setup is {setup_name}",
]

def tick(server):
    pass


def event(server, event):
    if event.type == EventType.authenticated:
        for message in messages:
            event.member.send_chat(
                message.format(
                    setup_name=server.get_current_setup_name()
                )
            )
