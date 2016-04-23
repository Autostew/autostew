import datetime
import json
import logging
from datetime import timedelta
from time import time, sleep

from decorator import decorator
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils import timezone

import autostew_web_session
from autostew_back.event_handlers.collision import HandleCollision
from autostew_back.event_handlers.ignored_events import HandleIgnore
from autostew_back.event_handlers.lap import HandleLap
from autostew_back.event_handlers.notification_leader_entered_last_lap import HandleNotificationLeaderEnteredLastLap
from autostew_back.event_handlers.notification_new_session_start import HandleNotificationNewSessionStart
from autostew_back.event_handlers.notification_presentation import HandleNotificationPresentation
from autostew_back.event_handlers.notification_race_start import HandleNotificationRaceStart
from autostew_back.event_handlers.notification_welcome import HandleNotificationWelcome
from autostew_back.event_handlers.notification_winner_finished_race import HandleNotificationWinnerFinishedRace
from autostew_back.event_handlers.player_left import HandlePlayerLeft
from autostew_back.event_handlers.race_lap_snapshot import HandleRaceLapSnapshot
from autostew_back.event_handlers.result import HandleResult
from autostew_back.event_handlers.sector import HandleSector
from autostew_back.event_handlers.session_end import HandleSessionEnd
from autostew_back.event_handlers.session_start import HandleSessionStart
from autostew_back.event_handlers.stage_change import HandleStageChange
from autostew_back.event_handlers.to_track import HandleToTrack
from autostew_back.ds_api import api_translations
from autostew_back.ds_api.api import ApiCaller
from autostew_back.ds_api.api_connector import ApiConnector
from autostew_web_enums.models import SessionState, EventDefinition, GameModeDefinition, TireWearDefinition, \
    PenaltyDefinition, ParticipantAttributeDefinition, FuelUsageDefinition, SessionAttributeDefinition, \
    AllowedViewsDefinition, PlayerFlagDefinition, WeatherDefinition, DamageDefinition, SessionFlagDefinition, \
    MemberAttributeDefinition, PrivacyDefinition
from autostew_web_session.models import models as session_models
from autostew_web_session.models.member import Member
from autostew_web_session.models.event import Event
from autostew_web_session.models.models import Track, Vehicle, VehicleClass, Livery
from autostew_web_session.models.participant import Participant
from autostew_web_session.models.session import SessionSetup
from autostew_web_users.models import SteamUser


class NoSessionSetupTemplateAvailableException(Exception):
    pass


class ServerState(models.Model):
    running = "Running"
    allocating = "Allocating"
    idle = "Idle"
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Server(models.Model):
    class Meta:
        ordering = ('name', )

    name = models.CharField(max_length=50, unique=True,
                            help_text='To successfully rename a server you will need to change it\'s settings too')
    contact = models.EmailField(blank=True)
    api_url = models.CharField(max_length=200,
                               help_text="Dedicated Server HTTP API URL, like http://user:pwd@host:port/")

    back_verified = models.BooleanField(default=False)
    back_enabled = models.BooleanField(default=False)
    back_reconnect = models.BooleanField(default=True)
    back_kicks = models.BooleanField(default=True)
    back_crash_points_limit = models.IntegerField(default=4000)
    back_crash_points_limit_ban_seconds = models.IntegerField(default=0, help_text="In seconds")
    back_safety_rating = models.BooleanField(default=True)
    back_performance_rating = models.BooleanField(default=True)
    back_custom_motd = models.CharField(max_length=200, blank=True)
    back_minimal_safety_class = models.ForeignKey('autostew_web_users.SafetyClass', null=True, blank=True)

    setup_rotation_index = models.IntegerField(default=0)
    setup_rotation = models.ManyToManyField('SessionSetup',
                                            related_name='rotated_in_server', through='SetupRotationEntry',
                                            help_text="Setups that will be used on this server's rotation")

    setup_queue = models.ManyToManyField('SessionSetup',
                                         related_name='queued_in_server', through='SetupQueueEntry',
                                         blank=True,
                                         help_text="If set, this will be the next setup used")

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

    def get_latest_sessions(self, limit=10):
        return reversed(self.session_set.filter(finished=True, parent=None))[:limit]

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

    @transaction.atomic
    def back_pull_lists(self, lists):
        for event in lists['events']['list']:
            if not EventDefinition.objects.filter(name=event['name']).exists():
                EventDefinition.objects.create(**event)
        for track in lists['tracks']['list']:
            if not Track.objects.filter(ingame_id=track['id']).exists():
                Track.objects.create(ingame_id=track['id'], name=track['name'], grid_size=track['gridsize'])
        for vehicle_class in lists['vehicle_classes']['list']:
            if not VehicleClass.objects.filter(ingame_id=vehicle_class['value']).exists():
                VehicleClass.objects.create(ingame_id=vehicle_class['value'], name=vehicle_class['name'])
        for vehicle in lists['liveries']['list']:
            try:
                vehicle_in_db = Vehicle.objects.get(ingame_id=vehicle['id'])
            except Vehicle.DoesNotExist:
                vehicle_in_db = Vehicle.objects.create(
                    ingame_id=vehicle['id'],
                    name=vehicle['name'],
                    vehicle_class=VehicleClass.objects.get(name=vehicle['class'])
                )
            for livery in vehicle['liveries']:
                if not Livery.objects.filter(vehicle__ingame_id=vehicle['id'], id_for_vehicle=livery['id']).exists():
                    Livery.objects.create(vehicle=vehicle_in_db, name=livery['name'], id_for_vehicle=livery['id'])
        for game_mode in lists['enums/game_mode']['list']:
            if not GameModeDefinition.objects.filter(ingame_id=game_mode['value']).exists():
                GameModeDefinition.objects.create(ingame_id=game_mode['value'], name=game_mode['name'])
        for tire_wear in lists['enums/tire_wear']['list']:
            if not TireWearDefinition.objects.filter(ingame_id=tire_wear['value']).exists():
                TireWearDefinition.objects.create(ingame_id=tire_wear['value'], name=tire_wear['name'])
        for penalty in lists['enums/penalties']['list']:
            if not PenaltyDefinition.objects.filter(ingame_id=penalty['value']).exists():
                PenaltyDefinition.objects.create(ingame_id=penalty['value'], name=penalty['name'])
        for participant_attribute in lists['attributes/participant']['list']:
            if not ParticipantAttributeDefinition.objects.filter(name=participant_attribute['name']).exists():
                ParticipantAttributeDefinition.objects.create(**participant_attribute)
        for fuel_usage in lists['enums/fuel_usage']['list']:
            if not FuelUsageDefinition.objects.filter(ingame_id=fuel_usage['value']).exists():
                FuelUsageDefinition.objects.create(ingame_id=fuel_usage['value'], name=fuel_usage['name'])
        for session_attribute in lists['attributes/session']['list']:
            if not SessionAttributeDefinition.objects.filter(name=session_attribute['name']).exists():
                SessionAttributeDefinition.objects.create(**session_attribute)
        for allowed_view in lists['enums/allowed_view']['list']:
            if not AllowedViewsDefinition.objects.filter(ingame_id=allowed_view['value']).exists():
                AllowedViewsDefinition.objects.create(ingame_id=allowed_view['value'], name=allowed_view['name'])
        for player_flag in lists['flags/player']['list']:
            if not PlayerFlagDefinition.objects.filter(ingame_id=player_flag['value']).exists():
                PlayerFlagDefinition.objects.create(ingame_id=player_flag['value'], name=player_flag['name'])
        for weather in lists['enums/weather']['list']:
            if not WeatherDefinition.objects.filter(ingame_id=weather['value']).exists():
                WeatherDefinition.objects.create(ingame_id=weather['value'], name=weather['name'])
        for damage in lists['enums/damage']['list']:
            if not DamageDefinition.objects.filter(ingame_id=damage['value']).exists():
                DamageDefinition.objects.create(ingame_id=damage['value'], name=damage['name'])
        for member_attribute in lists['attributes/member']['list']:
            if not MemberAttributeDefinition.objects.filter(name=member_attribute['name']).exists():
                MemberAttributeDefinition.objects.create(**member_attribute)
        for session_flag in lists['flags/session']['list']:
            if not SessionFlagDefinition.objects.filter(ingame_id=session_flag['value']).exists():
                SessionFlagDefinition.objects.create(ingame_id=session_flag['value'], name=session_flag['name'])
        PrivacyDefinition.objects.get_or_create(ingame_id=0, defaults={'name': 'Public'})
        PrivacyDefinition.objects.get_or_create(ingame_id=1, defaults={'name': 'Friends only'})
        PrivacyDefinition.objects.get_or_create(ingame_id=2, defaults={'name': 'Private'})

    def back_init_env(self, settings):
        self.settings = settings
        self.back_init_api(False, settings)
        self.back_pull_lists(self.api.get_lists())

    def back_start(self, settings, api_record=False):
        self.last_status_update_time = None
        self.settings = settings
        self.running = True
        self.current_session = None
        self.save()

        self.back_init_api(api_record, settings)
        self.back_pull_lists(self.api.get_lists())
        self.back_pull_server_status(self.api.get_status())
        self.send_chat("Autostew starting...")

        if self.state.name == ServerState.running:
            self.back_start_session()
        self.last_status_update_time = time()
        self.save()

    def back_init_api(self, api_record, settings):
        if getattr(self, 'api', None) is None:
            self.api = ApiCaller(
                self,
                record_destination=settings.api_record_destination if api_record is True else api_record
            )

    def back_pull_session_setup(self):
        new_setup = SessionSetup()
        connector = ApiConnector(self.api, new_setup, api_translations.session_setup)
        connector.pull_from_game(self.api.get_status(members=False, participants=False)['attributes'])
        new_setup.is_template = False
        new_setup.save()
        return new_setup

    def back_pull_session_status(self, status):
        if self.current_session:
            connector = ApiConnector(self.api, self.current_session, api_translations.session)
            connector.pull_from_game(status)
            self.current_session.save()

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
        self.back_pull_session_status(status)
        self.back_pull_members(status)
        self.back_pull_participants(status)

    def back_pull_members(self, status):
        for in_game_member in status['members']:
            pulled_member = Member()
            connector = ApiConnector(self.api, pulled_member, api_translations.member)
            connector.pull_from_game(in_game_member)
            try:
                existing_member = Member.objects.get(
                    session=self.current_session,
                    steam_id=pulled_member.steam_id
                )
                existing_member.steam_user.display_name = pulled_member.name
                existing_member.vehicle = pulled_member.vehicle
                existing_member.livery = pulled_member.livery
                existing_member.name = pulled_member.name
                existing_member.refid = pulled_member.refid
                pulled_member = existing_member
            except Member.DoesNotExist:
                try:
                    pulled_member.steam_user = SteamUser.objects.get(steam_id=pulled_member.steam_id)
                    pulled_member.steam_user.save()
                except SteamUser.DoesNotExist:
                    pulled_member.steam_user = SteamUser.objects.create(
                        steam_id=pulled_member.steam_id,
                        display_name=pulled_member.name
                    )
                    pulled_member.steam_user.update_safety_class()
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

    def get_participant(self, participant_id, refid=None):
        if not self.current_session:
            return None
        if refid is None:
            return self.current_session.participant_set.get(
                session=self.current_session,
                ingame_id=participant_id,
                still_connected=True
            )
        else:
            return self.current_session.participant_set.get(
                session=self.current_session,
                refid=refid,
                ingame_id=participant_id,
                still_connected=True
            )

    def get_member(self, refid):
        if not self.current_session:
            return None
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
            pulled_participant.member = self.get_member(pulled_participant.refid)
            if not pulled_participant.is_player:
                pulled_participant.member = None
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
                participant.race_position = 0
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
        return self.setup_rotation.all()[self.setup_rotation_index]

    def back_start_session(self):
        setup_template = self.back_get_next_setup()
        connector = ApiConnector(self.api, setup_template, api_translations.session_setup)
        connector.push_to_game('session')
        actual_setup = self.back_pull_session_setup()
        actual_setup.name = setup_template.name

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
        return Event.objects.filter(session=self.current_session, retries_remaining__gt=0, handled=False)

    def back_poll_loop(self, event_offset=None, only_one_run=False, one_by_one=False):
        if not only_one_run:
            logging.info("Entering event loop")
        if event_offset is None:
            self.api.reset_event_offset()
        else:
            self.api.event_offset = event_offset

        while True:
            with transaction.atomic():
                tick_start = time()

                self.update_player_latency()
                if self.current_session:
                    self.clock()
                    if not self.current_session.is_result:
                        self.back_full_pull()

                self.ping()

                new_events = self.api.get_new_events()
                logging.debug("Got {} new events".format(len(new_events)))

                for raw_event in new_events:
                    new_event = Event()
                    new_event.raw = json.dumps(raw_event)
                    new_event.session = self.current_session
                    connector = ApiConnector(self.api, new_event, api_translations.event_base)
                    connector.pull_from_game(raw_event)
                    new_event.event_parse(self)
                    new_event.save()

                for event in list(self.get_queued_events()):
                    if one_by_one:
                        input("Processing event {}".format(event))
                    event.handle(self)
                    self.refresh_from_db()

                if one_by_one:
                    input("Tick (enter)")

                sleep_time = self.settings.event_poll_period - (time() - tick_start)
                if sleep_time > 0:
                    sleep(sleep_time)

                if only_one_run:
                    return

    @staticmethod
    def get_event_handlers():
        return [
            HandleCollision,
            HandleLap,
            HandleNotificationLeaderEnteredLastLap,
            HandleNotificationNewSessionStart,
            HandleNotificationPresentation,
            HandleNotificationRaceStart,
            HandleNotificationWelcome,
            HandleNotificationWinnerFinishedRace,
            HandlePlayerLeft,
            HandleRaceLapSnapshot,
            HandleResult,
            HandleSector,
            HandleSessionEnd,
            HandleSessionStart,
            HandleStageChange,
            HandleToTrack,
            HandleIgnore
        ]

    def clock(self):
        if (
                        self.current_session.current_hour != getattr(self, 'hour', None) and
                        self.current_session.session_state.name == SessionState.race
        ):
            self.hour = self.current_session.current_hour
            self.api.send_chat("")
            self.api.send_chat("CLOCK {}:{:02d}".format(
                self.current_session.current_hour,
                self.current_session.current_minute)
            )

    def ping(self):
        self.last_ping = timezone.make_aware(datetime.datetime.now())
        self.save()

    def update_player_latency(self):
        if self.current_session is None or len(self.current_session.member_set.all()) == 0:
            self.average_player_latency = None
        else:
            self.average_player_latency = sum([member.ping for member in self.current_session.member_set.all()]) / len(
                self.current_session.member_set.all())

    def send_chat(self, message, refid=None):
        return self.api.send_chat(message, refid)

    def kick(self, refid, ban_seconds):
        return self.api.kick(refid, ban_seconds)

    def back_destroy(self):
        if self.current_session:
            self.current_session.running = False
            self.current_session.save()
        self.running = False
        self.save()

    def back_close_session(self):
        self.current_session.finished = True
        self.current_session.running = False
        self.current_session.save()

        for member in self.current_session.member_set.all():
            member.steam_user.push_elo_rating()

        for member in self.current_session.get_members_who_participated():
            for opponent in self.current_session.get_members_who_participated():
                if member == opponent:
                    continue
                member.steam_user.update_elo_rating(
                    opponent.steam_user,
                    self._versus_result(member, opponent)
                )

        self.current_session = None
        self.save()

    def _versus_result(self, member: Member, opponent: Member) -> float:
        if not self.current_session.get_members_who_finished_race():
            return None
        member_stayed = member in self.current_session.get_members_who_finished_race()
        opponent_stayed = opponent in self.current_session.get_members_who_finished_race()

        if not member_stayed and not opponent_stayed:
            return 0.5
        if member_stayed and not opponent_stayed:
            return 1
        if opponent_stayed and not member_stayed:
            return 0
        if member_stayed and opponent_stayed:
            if member.get_participant(self.current_session).race_position < opponent.get_participant(self.current_session).race_position:
                return 1
            else:
                return 0

