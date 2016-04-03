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
    allocating = "Allocating"
    idle = "Idle"


class BreakPluginLoadingException(Exception):
    pass


class UnmetPluginDependency(Exception):
    pass


class Server:
    def __init__(self, settings, env_init=False, api_record=False):
        self.get_current_setup_name = None  # Plugins set this to a function
        self.last_status_update_time = None
        self.state = None
        self.lobby_id = None
        self.joinable = None
        self.max_member_count = None

        self.settings = settings
        self.api = ApiCaller(
            self,
            record_destination=settings.api_record_destination if api_record is True else api_record
        )
        self.lists = ListGenerator(self.api).generate_all()
        self.session = Session(self.lists[ListName.session_attributes], self.lists, self.api)
        self.members = MemberList(self.lists[ListName.member_attributes], self.lists, self.api)
        self.participants = ParticipantList(self.lists[ListName.participant_attributes], self.lists, self.api)
        self.fetch_status()
        self._init_plugins(env_init)

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
                logging.info("Loading plugin {}.".format(plugin.name))
                if 'dependencies' in dir(plugin):
                    for dependency in plugin.dependencies:
                        if dependency not in self.settings.plugins[:index]:
                            raise UnmetPluginDependency
                if env_init:
                    self.env_init_plugins(plugin)
                    continue
                if 'init' in dir(plugin):
                    plugin.init(self)
        except BreakPluginLoadingException:
            pass

    @log_time
    def env_init_plugins(self, plugin):
        logging.info("Initializing environment for plugin {}.".format(plugin.name))
        if 'env_init' in dir(plugin):
            plugin.env_init(self)

    def poll_loop(self, event_offset=None, only_one_run=False, one_by_one=False):
        if not only_one_run:
            logging.info("Entering event loop")
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
                event = event_factory(raw_event, self)

                if one_by_one:
                    input("Event (enter)")

                if not updated_status_in_this_tick and event.reload_full_status:
                    self.fetch_status()
                    updated_status_in_this_tick = True

                for plugin in self.settings.plugins:
                    if 'event' in dir(plugin):
                        plugin.event(self, event)

            if time() - self.last_status_update_time > self.settings.full_update_period:
                self.fetch_status()

            if one_by_one:
                input("Tick (enter)")

            for plugin in self.settings.plugins:
                if 'tick' in dir(plugin):
                    plugin.tick(self)

            sleep_time = self.settings.event_poll_period - (time() - tick_start)
            if sleep_time > 0:
                sleep(sleep_time)

            if only_one_run:
                return

    def destroy(self):  # TODO consider using destructor
        for plugin in reversed(self.settings.plugins):
            if 'destroy' in dir(plugin):
                plugin.destroy(self)
