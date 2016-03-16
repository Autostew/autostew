"""
Allows player to set personal settings with chat commands, stored in the DB.
"""
from autostew_back.gameserver.event import BaseEvent, EventType
from autostew_back.gameserver.server import Server

command_prefix = "AS "


def event(server: Server, event: BaseEvent):
    if event.type == EventType.player_chat:
        if event.message.startswith(command_prefix):
            player_command(event.message[len(command_prefix):])
            # TODO get message sender