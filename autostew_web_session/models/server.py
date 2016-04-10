import datetime
import logging
from datetime import timedelta
from time import time, sleep

from decorator import decorator
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from autostew_back.gameserver.api import ApiCaller
from autostew_back.gameserver.event import event_factory
from autostew_back.gameserver.lists import ListGenerator, ListName
from autostew_back.gameserver.member import MemberList
from autostew_back.gameserver.participant import ParticipantList
from autostew_back.gameserver.session import Session
from autostew_web_session.models import models as session_models


@decorator
def log_time(f, *args, **kwargs):
    start_time = time()
    f(*args, **kwargs)
    logging.info("Plugin init took {} seconds".format(timedelta(seconds=time()-start_time)))


class BreakPluginLoadingException(Exception):
    pass


class UnmetPluginDependency(Exception):
    pass


class ServerState(models.Model):
    running = "Running"
    allocating = "Allocating"
    idle = "Idle"
    name = models.CharField(max_length=50)


class Server(models.Model):
    class Meta:
        ordering = ('name', )

    name = models.CharField(max_length=50, unique=True,
                            help_text='To successfully rename a server you will need to change it\'s settings too')
    api_url = models.CharField(max_length=200,
                               help_text="Dedicated Server HTTP API URL, like http://user:pwd@host:port/")

    setup_rotation_index = models.IntegerField()
    setup_rotation = models.ManyToManyField('SessionSetup',
                                            related_name='rotated_in_server', through='SetupRotationEntry',
                                            help_text="Setups that will be used on this server's rotation")

    setup_queue = models.ManyToManyField('SessionSetup',
                                         related_name='queued_in_server', through='SetupQueueEntry',
                                         blank=True,
                                         help_text="If set, this will be the next setup used")

    scheduled_sessions = models.ManyToManyField('Session', limit_choices_to={'planned': True},
                                                related_name='schedule_at_servers',
                                                blank=True,
                                                help_text="These schedule setups will be used (on their scheduled time)")

    running = models.BooleanField(help_text="This value should not be changed manually")
    current_session = models.ForeignKey('Session', null=True, related_name='+', blank=True)
    last_ping = models.DateTimeField(null=True, blank=True,
                                     help_text="Last time the server reported to be alive")
    average_player_latency = models.IntegerField(null=True, blank=True)
    joinable_internal = models.BooleanField(default=False)
    state = models.ForeignKey('ServerState', null=True, blank=True)
    lobby_id = models.CharField(max_length=50, blank=True)
    max_member_count = models.IntegerField(default=0)

    @property
    def is_up(self):
        return self.running and self.time_since_last_ping < 120

    @property
    def time_since_last_ping(self):
        return int((timezone.now() - self.last_ping).total_seconds())

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('session:server', args=[str(self.name)])

    def pop_next_queued_setup(self, peek=False):
        ordered_queue = session_models.SetupQueueEntry.objects.filter(server=self).order_by('order')
        if len(ordered_queue) == 0:
            return None
        next_setup = ordered_queue[0].setup
        if not peek:
            ordered_queue[0].delete()
        return next_setup

    def next_scheduled_session(self):
        for scheduled_session_it in self.scheduled_sessions.filter(running=False, finished=False):
            if (
                (not scheduled_session_it.schedule_date or scheduled_session_it.schedule_date == datetime.date.today()) and
                scheduled_session_it.schedule_time + datetime.timedelta(seconds=300) > datetime.time()
            ):
                return scheduled_session_it
        return None

    def back_start(self, settings, env_init=False, api_record=False):
        self.get_current_setup_name = None  # Plugins set this to a function
        self.last_status_update_time = None
        self.settings = settings

        self.api = ApiCaller(
            self,
            record_destination=settings.api_record_destination if api_record is True else api_record
        )
        self.lists = ListGenerator(self.api).generate_all()
        self.session_api = Session(self.lists[ListName.session_attributes], self.lists, self.api)
        self.members_api = MemberList(self.lists[ListName.member_attributes], self.lists, self.api)
        self.participants_api = ParticipantList(self.lists[ListName.participant_attributes], self.lists, self.api)
        self.back_fetch_status()
        self._back_init_plugins(env_init)

    def back_fetch_status(self):
        status = self.api.get_status()
        self.state = ServerState.objects.get_or_create(name=status['state'])[0]
        self.lobby_id = status['lobbyid']
        self.joinable_internal = status['joinable']
        self.max_member_count = status['max_member_count']
        self.session_api.update_from_game(status['attributes'])
        self.members_api.update_from_game(status['members'])
        self.participants_api.update_from_game(status['participants'])
        self.last_status_update_time = time()

    def _back_init_plugins(self, env_init):
        try:
            for index, plugin in enumerate(self.settings.plugins):
                logging.info("Loading plugin {}.".format(plugin.name))
                if 'dependencies' in dir(plugin):
                    for dependency in plugin.dependencies:
                        if dependency not in self.settings.plugins[:index]:
                            raise UnmetPluginDependency
                if env_init:
                    self._back_env_init_plugins(plugin)
                    continue
                if 'init' in dir(plugin):
                    plugin.init(self)
        except BreakPluginLoadingException:
            pass

    @log_time
    def _back_env_init_plugins(self, plugin):
        logging.info("Initializing environment for plugin {}.".format(plugin.name))
        if 'env_init' in dir(plugin):
            plugin.env_init(self)

    def _back_poll_loop(self, event_offset=None, only_one_run=False, one_by_one=False):
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
                    self.back_fetch_status()
                    updated_status_in_this_tick = True

                for plugin in self.settings.plugins:
                    if 'event' in dir(plugin):
                        plugin.event(self, event)

            if time() - self.last_status_update_time > self.settings.full_update_period:
                self.back_fetch_status()

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

    def back_destroy(self):
        for plugin in reversed(self.settings.plugins):
            if 'destroy' in dir(plugin):
                plugin.destroy(self)
