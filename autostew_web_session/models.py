from django.db import models


class Track(models.Model):
    ingame_id = models.IntegerField(help_text='pCars internal ID')
    name = models.CharField(max_length=100)
    grid_size = models.SmallIntegerField()

    def __str__(self):
        return self.name


class VehicleClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')
    vehicle_class = models.ForeignKey(VehicleClass)

    def __str__(self):
        return self.name


class Livery(models.Model):
    name = models.CharField(max_length=50)
    id_for_vehicle = models.IntegerField(help_text='pCars internal ID')
    vehicle = models.ForeignKey(Vehicle)

    def __str__(self):
        return "{} for {}".format(self.name, self.vehicle.name)


class ServerConfiguration(models.Model):
    pass


class SessionSetup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    server_controls_setup = models.BooleanField()
    server_controls_track = models.BooleanField()
    server_controls_vehicle_class = models.BooleanField()
    server_controls_vehicle = models.BooleanField()
    grid_size = models.IntegerField()
    max_players = models.IntegerField()
    opponent_difficulty = models.IntegerField()

    force_identical_vehicles = models.BooleanField()
    allow_custom_vehicle_setup = models.BooleanField()
    force_realistic_driving_aids = models.BooleanField()
    abs_allowed = models.BooleanField()
    sc_allowed = models.BooleanField()
    tcs_allowed = models.BooleanField()
    force_manual = models.BooleanField()
    rolling_starts = models.BooleanField()
    force_same_vehicle_class = models.BooleanField()
    fill_session_with_ai = models.BooleanField()
    mechanical_failures = models.BooleanField()
    auto_start_engine = models.BooleanField()
    timed_race = models.BooleanField()
    ghost_griefers = models.BooleanField()
    enforced_pitstop = models.BooleanField()

    practice1_length = models.IntegerField()
    practice2_length = models.IntegerField()
    qualify_length = models.IntegerField()
    warmup_length = models.IntegerField()
    race1_length = models.IntegerField()
    race2_length = models.IntegerField()

    public = models.BooleanField()
    friends_can_join = models.BooleanField()
    damage = models.ForeignKey('autostew_web_enums.DamageDefinition', null=True)
    tire_wear = models.ForeignKey('autostew_web_enums.TireWearDefinition', null=True)
    fuel_usage = models.ForeignKey('autostew_web_enums.FuelUsageDefinition', null=True)
    penalties = models.ForeignKey('autostew_web_enums.PenaltyDefinition', null=True)
    allowed_views = models.ForeignKey('autostew_web_enums.AllowedViewsDefinition', null=True)
    track = models.ForeignKey(Track, null=True)
    vehicle_class = models.ForeignKey(VehicleClass, null=True)
    vehicle = models.ForeignKey(Vehicle, null=True)
    date_year = models.IntegerField()
    date_month = models.IntegerField()
    date_day = models.IntegerField()
    date_hour = models.IntegerField()
    date_minute = models.IntegerField()
    date_progression = models.IntegerField()
    weather_progression = models.IntegerField()
    weather_slots = models.IntegerField()
    weather_1 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True)
    weather_2 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True)
    weather_3 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True)
    weather_4 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True)
    game_mode = models.ForeignKey('autostew_web_enums.GameModeDefinition', related_name='+', null=True)
    track_latitude = models.IntegerField()  # TODO this should be on track model
    track_longitude = models.IntegerField()  # TODO this should be on track model
    track_altitude = models.IntegerField()  # TODO this should be on track model

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=50, unique=True)
    session_setups = models.ManyToManyField(SessionSetup)

    running = models.BooleanField()
    # TODO joinable = models.BooleanField()
    # TODO state = server.state!!

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Session(models.Model):
    class Meta:
        ordering = ['start_timestamp']
    server = models.ForeignKey(Server)
    setup = models.ForeignKey(SessionSetup)

    start_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)
    planned = models.BooleanField()
    running = models.BooleanField()  # TODO join these to one
    finished = models.BooleanField()  # TODO join these to one

    lobby_id = models.CharField(max_length=200)
    max_member_count = models.IntegerField()

    first_snapshot = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    current_snapshot = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    starting_snapshot_lobby = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    starting_snapshot_to_track = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    starting_snapshot_practice1 = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    starting_snapshot_practice2 = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    starting_snapshot_qualifying = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    starting_snapshot_warmup = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    starting_snapshot_race = models.ForeignKey("SessionSnapshot", null=True, related_name='+')
    ending_snapshot_race = models.ForeignKey("SessionSnapshot", null=True, related_name='+')


class SessionSnapshot(models.Model):
    class Meta:
        ordering = ['timestamp']
    session = models.ForeignKey(Session)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_state = models.CharField(max_length=15)  # TODO these 3 are ugly
    session_stage = models.CharField(max_length=15)
    session_phase = models.CharField(max_length=15)
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


class Member(models.Model):
    session = models.ForeignKey(Session)
    still_connected = models.BooleanField()

    vehicle = models.ForeignKey(Vehicle)
    livery = models.ForeignKey(Livery)
    refid = models.IntegerField()
    steam_id = models.CharField(max_length=200)
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
    member = models.ForeignKey(Member)
    snapshot = models.ForeignKey(SessionSnapshot)
    still_connected = models.BooleanField()
    load_state = models.CharField(max_length=15)  # TODO check if this is correct
    ping = models.IntegerField()
    index = models.IntegerField()
    state = models.CharField(max_length=30)  # TODO this is ugly
    join_time = models.IntegerField()
    host = models.BooleanField()


class Participant(models.Model):
    member = models.ForeignKey(Member, null=True)  # AI will be NULL
    session = models.ForeignKey(Session)
    still_connected = models.BooleanField()

    ingame_id = models.IntegerField()
    refid = models.IntegerField()
    name = models.CharField(max_length=200)
    is_ai = models.BooleanField()
    vehicle = models.ForeignKey(Vehicle, null=True)  # NULL because AI owner change will do that
    livery = models.ForeignKey(Livery, null=True)  # NULL because AI owner change will do that


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
    state = models.CharField(max_length=20)
    headlights = models.BooleanField()
    wipers = models.BooleanField()
    speed = models.IntegerField()
    gear = models.SmallIntegerField()
    rpm = models.IntegerField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    position_z = models.IntegerField()
    orientation = models.IntegerField()


class Event(models.Model):  # TODO add timestamp and index
    snapshot = models.ForeignKey(SessionSnapshot, null=True, related_name='+')
    definition = models.ForeignKey('autostew_web_enums.EventDefinition', null=True, related_name='+')  # may be NULL and a custom event! eg. by a plugin
    session = models.ForeignKey(SessionSnapshot)


class RaceLapSnapshot(models.Model):
    class Meta:
        ordering = ['lap']
    session = models.ForeignKey(Session)
    snapshot = models.ForeignKey(SessionSnapshot)
    lap = models.IntegerField()


class Lap(models.Model):
    class Meta:
        ordering = ['lap']
    session = models.ForeignKey(Session)
    session_stage = models.CharField(max_length=15)  # TODO this is ugly
    participant = models.ForeignKey(Participant)
    lap = models.IntegerField()
    count_this_lap = models.BooleanField()
    lap_time = models.IntegerField()
    position = models.IntegerField()
    sector1_time = models.IntegerField()
    sector2_time = models.IntegerField()
    sector3_time = models.IntegerField()
    distance_travelled = models.IntegerField()


class Sector(models.Model):
    class Meta:
        ordering = ['lap', 'sector']
    session = models.ForeignKey(Session)
    session_stage = models.CharField(max_length=15)  # TODO this is ugly
    participant = models.ForeignKey(Participant)
    lap = models.IntegerField()
    count_this_lap = models.BooleanField()
    sector = models.SmallIntegerField()
    sector_time = models.IntegerField()
