import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.aggregates import Sum, Max, Min
from django.utils import timezone

from autostew_web_enums import models as enum_models
from autostew_web_users.models import SteamUser


class Track(models.Model):
    class Meta:
        ordering = ['name']

    ingame_id = models.IntegerField(help_text='pCars internal ID')
    name = models.CharField(max_length=100)
    grid_size = models.SmallIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('session:track', args=[str(self.id)])


class VehicleClass(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')
    vehicle_class = models.ForeignKey(VehicleClass)

    def __str__(self):
        return self.name


class Livery(models.Model):
    class Meta:
        ordering = ['vehicle__name', 'name']
        verbose_name_plural = "Liveries"

    name = models.CharField(max_length=50)
    id_for_vehicle = models.IntegerField(help_text='pCars internal ID')
    vehicle = models.ForeignKey(Vehicle)

    def __str__(self):
        return "{} for {}".format(self.name, self.vehicle.name)


class ServerConfiguration(models.Model):
    pass


class SessionSetup(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=100, blank=True)
    is_template = models.BooleanField()

    server_controls_setup = models.BooleanField(
        help_text="If true, players won't be able to control the race setup")
    server_controls_track = models.BooleanField(
        help_text="If true, players won't be able to control track selection")
    server_controls_vehicle_class = models.BooleanField(
        help_text="If true, players won't be acle to control vehicle class selection")
    server_controls_vehicle = models.BooleanField(
        help_text="If true, players won't be able to access vehicle selection")
    grid_size = models.IntegerField(
        help_text="How many cars can be on the field, don't set it higher than the track's grid size")
    max_players = models.IntegerField(
        help_text="How many human players can join the game")
    opponent_difficulty = models.IntegerField(
        help_text="AI difficulty, 0 to 100")

    force_identical_vehicles = models.BooleanField()
    allow_custom_vehicle_setup = models.BooleanField()
    force_realistic_driving_aids = models.BooleanField()
    abs_allowed = models.BooleanField(
        help_text="Won't have any effect if force realistic driving aids is on")
    sc_allowed = models.BooleanField(
        help_text="Won't have any effect if force realistic driving aids is on")
    tcs_allowed = models.BooleanField(
        help_text="Won't have any effect if force realistic driving aids is on")
    force_manual = models.BooleanField(
        help_text="If true, only manual transmission will be allowed")
    rolling_starts = models.BooleanField(
        help_text="If true, the race will have a rolling start")
    force_same_vehicle_class = models.BooleanField()
    fill_session_with_ai = models.BooleanField()
    mechanical_failures = models.BooleanField()
    auto_start_engine = models.BooleanField()
    timed_race = models.BooleanField(
        "If true, race length will be measured in minutes")
    ghost_griefers = models.BooleanField()
    enforced_pitstop = models.BooleanField()

    practice1_length = models.IntegerField(help_text="In minutes")
    practice2_length = models.IntegerField(help_text="In minutes")
    qualify_length = models.IntegerField(help_text="In minutes")
    warmup_length = models.IntegerField(help_text="In minutes")
    race1_length = models.IntegerField(help_text="In laps or minutes")
    race2_length = models.IntegerField(help_text="In laps or minutes (this setting does not have any effect (yet?)")

    public = models.BooleanField(
        help_text="If true, this game will be listed in the multiplayer server search (implies friends_can_join)")
    friends_can_join = models.BooleanField(help_text="If true, the players' friend will be able to join")
    damage = models.ForeignKey('autostew_web_enums.DamageDefinition', null=True)
    tire_wear = models.ForeignKey('autostew_web_enums.TireWearDefinition', null=True)
    fuel_usage = models.ForeignKey('autostew_web_enums.FuelUsageDefinition', null=True)
    penalties = models.ForeignKey('autostew_web_enums.PenaltyDefinition', null=True)
    allowed_views = models.ForeignKey('autostew_web_enums.AllowedViewsDefinition', null=True)
    track = models.ForeignKey(Track, null=True, blank=True)
    vehicle_class = models.ForeignKey(VehicleClass, null=True, blank=True,
        help_text="Only has a real effect if force_same_vehicle_class")
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True,
        help_text="Only has a real effect if force_same_vehicle")
    date_year = models.IntegerField(help_text="Race date, set to 0 for 'real date'")
    date_month = models.IntegerField(help_text="Race date, set to 0 for 'real date'")
    date_day = models.IntegerField(help_text="Race date, set to 0 for 'real date'")
    date_hour = models.IntegerField()
    date_minute = models.IntegerField()
    date_progression = models.IntegerField(
        help_text="Time multiplier, unconfirmed allowed values: 0, 1, 2, 5, 10, 30, 60"
    )
    weather_progression = models.IntegerField(
        help_text="Weather progression multiplier, unconfirmed allowed values: 0, 1, 2, 5, 10, 30, 60"
    )
    weather_slots = models.IntegerField(
        help_text="Set to 0 for 'real weather'"
    )
    weather_1 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True, blank=True)
    weather_2 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True, blank=True)
    weather_3 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True, blank=True)
    weather_4 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True, blank=True)
    game_mode = models.ForeignKey('autostew_web_enums.GameModeDefinition', related_name='+', null=True, blank=True)
    track_latitude = models.IntegerField(
        help_text="Setting this value won't have any effect")  # TODO this should be on track model
    track_longitude = models.IntegerField(
        help_text="Setting this value won't have any effect")  # TODO this should be on track model
    track_altitude = models.IntegerField(
        help_text="Setting this value won't have any effect")  # TODO this should be on track model

    def __str__(self):
        return "{} ({})".format(self.name, "template" if self.is_template else "instance")


class Server(models.Model):
    class Meta:
        ordering = ('name', )

    name = models.CharField(max_length=50, unique=True,
                            help_text='To successfully rename a server you will need to change it\'s settings too')

    session_setups = models.ManyToManyField(SessionSetup, limit_choices_to={'is_template': True},
                                            related_name='rotated_in_server',
                                            help_text="Setups that will be used on this server's rotation")

    next_setup = models.ForeignKey(SessionSetup, limit_choices_to={'is_template': True}, related_name='next_in_server',
                                   null=True, blank=True,
                                   help_text="If set, this will be the next setup used")

    scheduled_sessions = models.ManyToManyField('Session', limit_choices_to={'planned': True},
                                                null=True, blank=True,
                                                related_name='schedule_at_servers',
                                                help_text="These schedule setups will be used (on their scheduled time)")

    running = models.BooleanField(help_text="This value should not be changed manually")
    current_session = models.ForeignKey('Session', null=True, related_name='+', blank=True)
    last_ping = models.DateTimeField(null=True, blank=True,
                                     help_text="Last time the server reported to be alive")
    average_player_latency = models.IntegerField(null=True, blank=True)
    # TODO joinable = models.BooleanField()
    # TODO state = server.state!!

    @property
    def time_since_last_ping(self):
        return int((timezone.now() - self.last_ping).total_seconds())

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('session:server', args=[str(self.name)])


class Session(models.Model):
    class Meta:
        ordering = ['start_timestamp']

    server = models.ForeignKey(Server)
    setup_template = models.ForeignKey(SessionSetup,  limit_choices_to={'is_template': True}, related_name='+',
                                       help_text="This setup is feeded to the game")
    setup_actual = models.ForeignKey(SessionSetup,  limit_choices_to={'is_template': False}, related_name='+',
                                     null=True, help_text="This setup is read from the game once the race starts")

    start_timestamp = models.DateTimeField(auto_now_add=True,
                                           help_text="Time when the race starts/started")
    last_update_timestamp = models.DateTimeField(auto_now=True)
    planned = models.BooleanField(help_text="If true, this race was/is scheduled")
    schedule_time = models.TimeField(null=True, blank=True, help_text="Time this schedule will run")
    schedule_date = models.DateField(null=True, blank=True,
                                     help_text="Date this schedule will run, if blank will run daily")
    running = models.BooleanField(help_text="If true, this race is currently running")
    finished = models.BooleanField(help_text="If true, this race finished")

    lobby_id = models.CharField(max_length=200)
    max_member_count = models.IntegerField()

    first_snapshot = models.ForeignKey("SessionSnapshot", null=True, blank=True, related_name='+')
    current_snapshot = models.ForeignKey("SessionSnapshot", null=True, blank=True, related_name='+')
    starting_snapshot_lobby = models.ForeignKey("SessionSnapshot", null=True, blank=True, related_name='+')
    starting_snapshot_to_track = models.ForeignKey("SessionSnapshot", null=True, blank=True, related_name='+')

    def get_absolute_url(self):
        return reverse('session:session', args=[str(self.id)])

    def __str__(self):
        return "{} - {}".format(self.id, self.setup_actual.name)


class SessionSnapshot(models.Model):
    class Meta:
        ordering = ['timestamp']

    session = models.ForeignKey(Session)
    is_result = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_state = models.ForeignKey("autostew_web_enums.SessionState")
    session_stage = models.ForeignKey("autostew_web_enums.SessionStage")
    session_phase = models.ForeignKey("autostew_web_enums.SessionPhase")
    session_time_elapsed = models.BigIntegerField()
    session_time_duration = models.IntegerField()
    num_participants_valid = models.IntegerField()
    num_participants_disq = models.IntegerField()
    num_participants_retired = models.IntegerField()
    num_participants_dnf = models.IntegerField()
    num_participants_finished = models.IntegerField()
    current_year = models.IntegerField()
    current_month = models.IntegerField()
    current_day = models.IntegerField()
    current_hour = models.IntegerField()
    current_minute = models.IntegerField()
    rain_density_visual = models.IntegerField()
    wetness_path = models.IntegerField()
    wetness_off_path = models.IntegerField()
    wetness_avg = models.IntegerField()
    wetness_predicted_max = models.IntegerField()
    wetness_max_level = models.IntegerField()
    temperature_ambient = models.IntegerField()
    temperature_track = models.IntegerField()
    air_pressure = models.IntegerField()

    def get_absolute_url(self):
        return reverse('session:snapshot', args=[str(self.id)])

    @property
    def previous_in_session(self):
        try:
            previous_timestamp = SessionSnapshot.objects.filter(
                timestamp__lt=self.timestamp,
                session=self.session,
            ).aggregate(Max('timestamp'))['timestamp__max']
            return SessionSnapshot.objects.get(
                timestamp=previous_timestamp,
                session=self.session
            )
        except self.DoesNotExist:
            return None

    @property
    def next_in_session(self):
        try:
            next_timestamp = SessionSnapshot.objects.filter(
                timestamp__gt=self.timestamp,
                session=self.session,
            ).aggregate(Min('timestamp'))['timestamp__min']
            return SessionSnapshot.objects.get(
                timestamp=next_timestamp,
                session=self.session
            )
        except self.DoesNotExist:
            return None


class SessionStage(models.Model):
    session = models.ForeignKey(Session, related_name='stages')
    stage = models.ForeignKey(enum_models.SessionStage)
    starting_snapshot = models.ForeignKey(SessionSnapshot, related_name='starting_of', null=True, blank=True)
    result_snapshot = models.ForeignKey(SessionSnapshot, related_name='result_of', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('session:session_stage', args=[str(self.session.id), str(self.stage.name)])


class Member(models.Model):
    class Meta:
        ordering = ['name']

    steam_user = models.ForeignKey(SteamUser)
    session = models.ForeignKey(Session)
    still_connected = models.BooleanField()

    vehicle = models.ForeignKey(Vehicle)
    livery = models.ForeignKey(Livery)
    refid = models.IntegerField()
    steam_id = models.CharField(max_length=200)  # TODO duplicate in SteamUser
    name = models.CharField(max_length=200)

    setup_used = models.BooleanField()
    controller_gamepad = models.BooleanField()  # TODO these 2 are ugly
    controller_wheel = models.BooleanField()
    aid_steering = models.BooleanField()
    aid_braking = models.BooleanField()
    aid_abs = models.BooleanField()
    aid_traction = models.BooleanField()
    aid_stability = models.BooleanField()
    aid_no_damage = models.BooleanField()
    aid_auto_gears = models.BooleanField()
    aid_auto_clutch = models.BooleanField()
    model_normal = models.BooleanField()  # TODO these 4 are ugly
    model_experienced = models.BooleanField()
    model_pro = models.BooleanField()
    model_elite = models.BooleanField()
    aid_driving_line = models.BooleanField()
    valid = models.BooleanField()  # idk what this means


class MemberSnapshot(models.Model):
    class Meta:
        ordering = ['member__name']

    member = models.ForeignKey(Member)
    snapshot = models.ForeignKey(SessionSnapshot)
    still_connected = models.BooleanField()
    load_state = models.ForeignKey(enum_models.MemberLoadState)
    ping = models.IntegerField()
    index = models.IntegerField()
    state = models.ForeignKey(enum_models.MemberState)
    join_time = models.IntegerField()
    host = models.BooleanField()


class Participant(models.Model):
    class Meta:
        ordering = ['name']

    member = models.ForeignKey(Member, null=True, blank=True)  # AI will be NULL
    session = models.ForeignKey(Session)
    still_connected = models.BooleanField()

    ingame_id = models.IntegerField()
    refid = models.IntegerField()
    name = models.CharField(max_length=200)
    is_ai = models.BooleanField()
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True)  # NULL because AI owner change will do that
    livery = models.ForeignKey(Livery, null=True, blank=True)  # NULL because AI owner change will do that

    def get_absolute_url(self):
        return reverse('session:participant', args=[str(self.session.id), str(self.ingame_id)])


class ParticipantSnapshot(models.Model):
    class Meta:
        ordering = ['race_position']

    snapshot = models.ForeignKey(SessionSnapshot)
    participant = models.ForeignKey(Participant)
    still_connected = models.BooleanField()

    grid_position = models.IntegerField()
    race_position = models.IntegerField()
    current_lap = models.IntegerField()
    current_sector = models.IntegerField()
    sector1_time = models.IntegerField()
    sector2_time = models.IntegerField()
    sector3_time = models.IntegerField()
    last_lap_time = models.IntegerField()
    fastest_lap_time = models.IntegerField()
    state = models.ForeignKey(enum_models.ParticipantState)
    headlights = models.BooleanField()
    wipers = models.BooleanField()
    speed = models.IntegerField()
    gear = models.SmallIntegerField()
    rpm = models.IntegerField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    position_z = models.IntegerField()
    orientation = models.IntegerField()
    total_time = models.IntegerField()

    def last_lap_is_fastest_in_shapshot(self):
        return self.last_lap_time <= self.snapshot.participantsnapshot_set.filter(last_lap_time__gt=0).aggregate(Min('last_lap_time'))['last_lap_time__min']

    def last_lap_is_fastest_in_race(self):
        return self.last_lap_time <= self.snapshot.participantsnapshot_set.filter(fastest_lap_time__gt=0).aggregate(Min('fastest_lap_time'))['fastest_lap_time__min']

    def fastest_lap_is_fastest_in_race(self):
        return self.fastest_lap_time <= self.snapshot.participantsnapshot_set.filter(fastest_lap_time__gt=0).aggregate(Min('fastest_lap_time'))['fastest_lap_time__min']

    def gap(self):
        if self.race_position == 1:
            return None
        if self.snapshot.session_stage.name.startswith("Race"):
            if not self.total_time:
                return None
            return self.total_time - ParticipantSnapshot.objects.get(snapshot=self.snapshot, race_position=1).total_time
        else:
            if not self.fastest_lap_time:
                return None
            return self.fastest_lap_time - ParticipantSnapshot.objects.get(snapshot=self.snapshot, race_position=1).fastest_lap_time


class Event(models.Model):
    class Meta:
        ordering = ['ingame_index']

    snapshot = models.ForeignKey(SessionSnapshot, null=True, blank=True, related_name='+')
    definition = models.ForeignKey('autostew_web_enums.EventDefinition', null=True, blank=True, related_name='+')  # may be NULL and a custom event! eg. by a plugin
    session = models.ForeignKey(Session)
    timestamp = models.DateTimeField()
    ingame_index = models.IntegerField()
    raw = models.TextField()


class RaceLapSnapshot(models.Model):
    class Meta:
        ordering = ['session_id', 'lap']

    session = models.ForeignKey(Session)
    snapshot = models.ForeignKey(SessionSnapshot, unique=True)
    lap = models.IntegerField()

    def get_absolute_url(self):
        return self.snapshot.get_absolute_url()


class Lap(models.Model):
    class Meta:
        ordering = ['session_id', 'lap']

    session = models.ForeignKey(Session)
    session_stage = models.ForeignKey(enum_models.SessionStage)
    participant = models.ForeignKey(Participant)
    lap = models.IntegerField()
    count_this_lap = models.BooleanField()
    lap_time = models.IntegerField()
    position = models.IntegerField()
    sector1_time = models.IntegerField()
    sector2_time = models.IntegerField()
    sector3_time = models.IntegerField()
    distance_travelled = models.IntegerField()

    def is_personal_sector1_race_best_in_stage(self):
        return self._best_in_stage_evaluation('sector1_time')

    def is_personal_sector2_race_best_in_stage(self):
        return self._best_in_stage_evaluation('sector2_time')

    def is_personal_sector3_race_best_in_stage(self):
        return self._best_in_stage_evaluation('sector3_time')

    def is_personal_race_best_in_stage(self):
        return self._best_in_stage_evaluation('lap_time')

    def _best_in_stage_evaluation(self, field_name):
        return getattr(self, field_name) <= self.participant.lap_set.filter(
            **{
                '{}__gt'.format(field_name): 0,
                'session_stage': self.session_stage
            }
        ).aggregate(Min(field_name))['{}__min'.format(field_name)]

class Sector(models.Model):
    class Meta:
        ordering = ['session_id', 'lap', 'sector']

    session = models.ForeignKey(Session)
    session_stage = models.ForeignKey(enum_models.SessionStage)
    participant = models.ForeignKey(Participant)
    lap = models.IntegerField()
    count_this_lap = models.BooleanField()
    sector = models.SmallIntegerField()
    sector_time = models.IntegerField()
