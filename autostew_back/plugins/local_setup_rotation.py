import logging

from autostew_back.gameserver.event import EventType, BaseEvent
from autostew_web_enums.models import SessionState
from autostew_web_session.models.server import Server

name = 'Local setup rotation'

setup_rotation = []
_setup_index = None
_server = None


def init(server: Server):
    global setup_rotation
    global _server
    _server = server
    server.get_current_setup_name = get_current_setup_name
    setup_rotation = server.settings.setup_rotation


def event(server: Server, event: BaseEvent):
    if event.type == EventType.state_changed:
        if event.new_state == SessionState.lobby:
            load_next_setup(server)


def load_next_setup(server: Server, index=None):
    global _setup_index
    if index is None:
        load_index = 0 if _setup_index is None else _setup_index + 1
    else:
        load_index = index
    if load_index >= len(server.settings.setup_rotation):
        load_index = 0
    logging.info("Loading setup {}: {}".format(load_index, server.settings.setup_rotation[load_index].name))
    server.settings.setup_rotation[load_index].make_setup(server)
    _setup_index = load_index


def get_current_setup_name():
    if _setup_index is None:
        return None
    return _server.settings.setup_rotation[_setup_index].name
