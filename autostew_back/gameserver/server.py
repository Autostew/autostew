import logging

from datetime import timedelta
from decorator import decorator
from enum import Enum
from time import time, sleep

from autostew_back.gameserver.api import ApiCaller
from autostew_back.gameserver.event import event_factory
from autostew_back.gameserver.lists import ListGenerator, ListName
from autostew_back.gameserver.member import MemberList
from autostew_back.gameserver.participant import ParticipantList
from autostew_back.gameserver.session import Session

@decorator
def log_time(f, *args, **kwargs):
    start_time = time()
    f(*args, **kwargs)
    logging.info("Plugin init took {} seconds".format(timedelta(seconds=time()-start_time)))


class ServerState(Enum):
    running = "Running"
    idle = "Idle"

class BreakPluginLoadingException(Exception):
    pass


class UnmetPluginDependency(Exception):
    pass


class Server:
    def __init__(self, settings, env_init):
        self.last_status_update_time = None
        self._setup_index = None
        self.state = None
        self.lobby_id = None
        self.joinable = None
        self.max_member_count = None

        self.settings = settings
        self.api = ApiCaller(self)
        self.lists = ListGenerator(self.api).generate_all()
        self.session = Session(self.lists[ListName.session_attributes], self.lists, self.api)
        self.members = MemberList(self.lists[ListName.member_attributes], self.lists, self.api)
        self.participants = ParticipantList(self.lists[ListName.participant_attributes], self.lists, self.api)
        self.fetch_status()
        self._init_plugins(env_init)
        self.load_next_setup(0)

    def fetch_status(self):
        status = self.api.get_status()
        self.state = ServerState(status['state'])
        self.lobby_id = status['lobbyid']
        self.joinable = status['joinable']
        self.max_member_count = status['max_member_count']
        self.session.update_from_game(status['attributes'])
        self.members.update_from_game(status['members'])
        self.participants.update_from_game(status['participants'])
        self.last_status_update_time = time()

    def _init_plugins(self, env_init):

        try:
            for index, plugin in enumerate(self.settings.plugins):
                self.env_init_plugins(env_init, plugin)
                logging.info("Loading plugin {}.".format(plugin.name))
                if 'dependencies' in dir(plugin):
                    for dependency in plugin.dependencies:
                        if dependency not in self.settings.plugins[:index]:
                            raise UnmetPluginDependency
                if 'init' in dir(plugin):
                    plugin.init(self)
        except BreakPluginLoadingException:
            pass

    @log_time
    def env_init_plugins(self, env_init, plugin):
        if env_init:
            logging.info("Initializing environment for plugin {}.".format(plugin.name))
            if 'env_init' in dir(plugin):
                plugin.env_init(self)

    def load_next_setup(self, index=None):
        if index is None:
            load_index = 0 if self._setup_index is None else self._setup_index + 1
        else:
            load_index = index
        if load_index >= len(self.settings.setup_rotation):
            load_index = 0
        logging.info("Loading setup {}: {}".format(load_index, self.settings.setup_rotation[load_index].__file__))
        self.settings.setup_rotation[load_index].make_setup(self)
        self._setup_index = load_index

    def get_current_setup_name(self):
        return self.settings.setup_rotation[self._setup_index].name

    def poll_loop(self, event_offset=None, only_one_run=False):
        if event_offset is None:
            self.api.reset_event_offset()
        else:
            self.api.event_offset = event_offset

        while True:
            tick_start = time()
            updated_status_in_this_tick = False

            events = self.api.get_new_events()
            logging.debug("Got {} events".format(len(events)))

            for raw_event in events:
                print(raw_event)
                event = event_factory(raw_event, self)

                if not updated_status_in_this_tick and event.reload_full_status:
                    self.fetch_status()
                    updated_status_in_this_tick = True

                for plugin in self.settings.plugins:
                    if 'event' in dir(plugin):
                        plugin.event(self, event)

            if time() - self.last_status_update_time > self.settings.full_update_period:
                self.fetch_status()

            for plugin in self.settings.plugins:
                if 'tick' in dir(plugin):
                    plugin.tick(self)

            sleep_time = self.settings.event_poll_period - (time() - tick_start)
            if sleep_time > 0:
                sleep(sleep_time)

            if only_one_run:
                return