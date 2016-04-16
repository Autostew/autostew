import datetime
import logging
from datetime import timedelta
from time import time, sleep

from decorator import decorator
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

import autostew_web_session
from autostew_back.gameserver import api_translations
from autostew_back.gameserver.api import ApiCaller
from autostew_back.gameserver.api_connector import ApiConnector
from autostew_back.plugins.db_session_writer_libs.db_safety_rating import initial_safety_rating
from autostew_web_enums.models import SessionState
from autostew_web_session.models import models as session_models
from autostew_web_session.models.member import Member
from autostew_web_session.models.models import Event
from autostew_web_session.models.participant import Participant
from autostew_web_session.models.session import SessionSetup
from autostew_web_users.models import SteamUser


@decorator
def log_time(f, *args, **kwargs):
    start_time = time()
    f(*args, **kwargs)
    logging.info("Plugin init took {} seconds".format(timedelta(seconds=time()-start_time)))


class NoSessionSetupTemplateAvailableException(Exception):
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
    contact = models.EmailField(blank=True)
    api_url = models.CharField(max_length=200,
                               help_text="Dedicated Server HTTP API URL, like http://user:pwd@host:port/")

    back_enabled = models.BooleanField(default=False)
    back_reconnect = models.BooleanField(default=True)
    back_kicks = models.BooleanField(default=False)
    back_crash_points_limit = models.BooleanField(default=4000)
    back_safety_rating = models.BooleanField(default=True)
    back_performance_rating = models.BooleanField(default=True)

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
    session_state = models.ForeignKey('autostew_web_enums.SessionState', null=True, blank=True)
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

    def back_start(self, settings, env_init=False, api_record=False):
        self.last_status_update_time = None
        self.settings = settings
        self.running = True

        self.api = ApiCaller(
            self,
            record_destination=settings.api_record_destination if api_record is True else api_record
        )
        self.back_pull_server_status(self.api.get_status())

        if self.state.name == ServerState.running:
            self.back_start_session()
        self.last_status_update_time = time()
        self.save()

    def back_pull_session_setup(self):
        new_setup = SessionSetup()
        connector = ApiConnector(self.api, new_setup, api_translations.session_setup)
        connector.pull_from_game(self.api.get_status(members=False, participants=False)['attributes'])
        new_setup.is_template = False
        new_setup.save()
        return new_setup

    def back_pull_server_status(self, status):  # TODO this should also be made over an API translator
        self.state = ServerState.objects.get_or_create(name=status['state'])[0]
        self.session_state = (
            SessionState.objects.get_or_create(name=status['attributes']['session_state'])[0]
            if 'attributes' in status.keys() and 'session_state' in status['attributes'].keys() else None)
        self.lobby_id = status['lobbyid']
        self.joinable_internal = status['joinable']
        self.max_member_count = status['max_member_count']
        self.save()

    def back_full_pull(self):
        status = self.api.get_status()
        self.back_pull_server_status(status)
        self.back_pull_members(status)
        self.back_pull_participants(status)

    def back_pull_members(self, status):  # TODO refactor this
        for in_game_member in status['members']:
            pulled_member = Member()
            connector = ApiConnector(self.api, pulled_member, api_translations.member)
            connector.pull_from_game(in_game_member)
            try:
                existing_member = Member.objects.get(
                    session=self.current_session,
                    refid=pulled_member.refid,
                    steam_id=pulled_member.steam_id,
                    still_connected=True
                )
                pulled_member.id = existing_member.id
            except Member.DoesNotExist:
                try:
                    pulled_member.steam_user = SteamUser.objects.get(steam_id=pulled_member.steam_id)
                except SteamUser.DoesNotExist:
                    pulled_member.steam_user = SteamUser.objects.create(
                        steam_id=pulled_member.steam_id,
                        display_name=pulled_member.name,
                        safety_rating=initial_safety_rating
                    )
                    pulled_member.steam_user.update_safety_class()
            pulled_member.steam_user.display_name = pulled_member.name
            pulled_member.steam_user.save()
            pulled_member.session = self.current_session
            pulled_member.still_connected = True
            pulled_member.save()

        for member in self.current_session.member_set.filter(still_connected=True):
            found = False
            for members_in_status in status['members']:
                if members_in_status['refid'] == member.refid and members_in_status['steamid'] == member.steam_id:
                    found = True
            if not found:
                member.still_connected = False
                member.save()

    def get_participant(self, refid, participant_id):
        return self.current_session.participant_set.get(
            session=self.current_session,
            refid=refid,
            ingame_id=participant_id,
            still_connected=True
        )

    def get_member(self, refid):
        return self.current_session.member_set.get(
            session=self.current_session,
            refid=refid,
            still_connected=True
        )

    def back_pull_participants(self, status):
        for in_game_participant in status['participants']:
            pulled_participant = Participant()
            connector = ApiConnector(self.api, pulled_participant, api_translations.participant)
            connector.pull_from_game(in_game_participant)
            try:
                existing_participant = Participant.objects.get(
                    session=self.current_session,
                    ingame_id=pulled_participant.ingame_id,
                    refid=pulled_participant.refid,
                    still_connected=True
                )
                pulled_participant.id = existing_participant.id
            except Participant.DoesNotExist:
                pass
            pulled_participant.session = self.current_session
            pulled_participant.still_connected = True
            pulled_participant.save()

        self.back_mark_disconnected_participants(status)

    def back_mark_disconnected_participants(self, status):
        for participant in self.current_session.participant_set.filter(still_connected=True):
            found = False
            for participant_in_status in status['participants']:
                if participant_in_status['attributes']['RefId'] == participant.refid and participant_in_status['id'] == participant.ingame_id:
                    found = True

            if not found:
                participant.still_connected = False
                participant.save()

    def back_get_next_setup(self):
        peek = (
            not self.session_state or
            self.session_state.name != SessionState.lobby or
            self.state != ServerState.running
        )

        queued_setup = self.pop_next_queued_setup(peek)
        if queued_setup:
            return queued_setup

        if not self.setup_rotation.exists():
            raise NoSessionSetupTemplateAvailableException("No setup rotation or queued!")
        if not peek:
            self.setup_rotation_index += 1
        if self.setup_rotation_index >= len(self.setup_rotation.all()):
            self.setup_rotation_index = 0
        self.save()
        return self.setup_rotation[self.setup_rotation_index]

    def back_start_session(self):
        setup_template = self.back_get_next_setup()
        connector = ApiConnector(self.api, setup_template, api_translations.session_setup)
        connector.push_to_game('session')
        actual_setup = self.back_pull_session_setup()

        session = autostew_web_session.models.session.Session(
            server=self,
            setup_template=setup_template,
            setup_actual=actual_setup,
            max_member_count=self.max_member_count,
            running=True,
            finished=False,
        )
        session.save()

        self.current_session = session
        self.save()

        self.back_full_pull()

        self.current_session.create_snapshot()
        self.save()
        return session

    def get_queued_events(self):
        return Event.objects.filter(session=self.current_session, retries_remaining__gt=0)

    def back_poll_loop(self, event_offset=None, only_one_run=False, one_by_one=False):
        if not only_one_run:
            logging.info("Entering event loop")
        if event_offset is None:
            self.api.reset_event_offset()
        else:
            self.api.event_offset = event_offset

        while True:
            tick_start = time()

            if self.current_session:
                self.back_full_pull()

            new_events = self.api.get_new_events()
            logging.debug("Got {} new events".format(len(new_events)))

            for raw_event in new_events:
                new_event = Event()
                new_event.session = self.current_session
                connector = ApiConnector(self.api, new_event, api_translations.event_base)
                connector.pull_from_game(raw_event)
                new_event.event_parse(self)

            for event in self.get_queued_events() + new_events:
                if one_by_one:
                    input("Processing event {}".format(event))
                event.handle(self)

            if one_by_one:
                input("Tick (enter)")

            sleep_time = self.settings.event_poll_period - (time() - tick_start)
            if sleep_time > 0:
                sleep(sleep_time)

            if only_one_run:
                return
