from django.db import models


class Track(models.Model):
    id = models.IntegerField(help_text='pCars internal ID', primary_key=True)
    name = models.CharField(max_length=100)
    grid_size = models.SmallIntegerField()

    def __str__(self):
        return self.name


class VehicleClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')
    vehicle_class = models.ForeignKey(VehicleClass)

    def __str__(self):
        return self.name


class Livery(models.Model):
    name = models.CharField(max_length=50)
    id_for_vehicle = models.IntegerField(help_text='pCars internal ID')
    vehicle = models.ForeignKey(Vehicle)

    def __str__(self):
        return "{} for {}".format(self.name, self.vehicle.name)


class EventDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    attributes = models.TextField(max_length=200)

    def __str__(self):
        return "{}-{}".format(self.type, self.name)


class GameModeDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class TireWearDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class PenaltyDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class FuelUsageDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name

class AllowedViewsDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class PlayerFlagDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class WeatherDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class DamageDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class SessionFlagDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class SessionAttributeDefinition(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class MemberAttributeDefinition(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ParticipantAttributeDefinition(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ServerConfiguration(models.Model):
    pass


class SessionConfiguration(models.Model):
    pass


class SetupRotation(models.Model):
    pass


class SessionSetup(models.Model):
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
    damage = models.ForeignKey(DamageDefinition)
    tire_wear = models.ForeignKey(TireWearDefinition)
    fuel_usage = models.ForeignKey(FuelUsageDefinition)
    penalties = models.ForeignKey(PenaltyDefinition)
    allowed_views = models.ForeignKey(AllowedViewsDefinition)
    track = models.ForeignKey(Track)
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
    weather_1 = models.ForeignKey(WeatherDefinition)
    weather_2 = models.ForeignKey(WeatherDefinition)
    weather_3 = models.ForeignKey(WeatherDefinition)
    weather_4 = models.ForeignKey(WeatherDefinition)
    game_mode = models.ForeignKey(GameModeDefinition)
    track_latitude = models.IntegerField()
    track_longitude = models.IntegerField()
    track_altitude = models.IntegerField()


class Server(models.Model):
    name = models.CharField(max_length=50, unique=True)
    running = models.BooleanField()

    def __str__(self):
        return self.name


class Session(models.Model):
    server = models.ForeignKey(Server)
    setup = models.ForeignKey(SessionSetup)

    planned = models.BooleanField()
    running = models.BooleanField()  # TODO join these to one
    finished = models.BooleanField()  # TODO join these to one

    first_snapshot = models.ForeignKey("SessionSnapshot", null=True)
    current_snapshot = models.ForeignKey("SessionSnapshot", null=True)
    starting_snapshot_lobby = models.ForeignKey("SessionSnapshot", null=True)
    starting_snapshot_to_track = models.ForeignKey("SessionSnapshot", null=True)
    starting_snapshot_practice1 = models.ForeignKey("SessionSnapshot", null=True)
    starting_snapshot_practice2 = models.ForeignKey("SessionSnapshot", null=True)
    starting_snapshot_qualifying = models.ForeignKey("SessionSnapshot", null=True)
    starting_snapshot_warmup = models.ForeignKey("SessionSnapshot", null=True)
    starting_snapshot_race = models.ForeignKey("SessionSnapshot", null=True)
    ending_snapshot_race = models.ForeignKey("SessionSnapshot", null=True)


class SessionSnapshot(models.Model):
    session = models.ForeignKey(Session)
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
    session = models.ForeignKey(SessionSnapshot)
    # TODO status = active, left

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


class MemberSnapshop(models.Model):
    member = models.ForeignKey(Member)

    load_state = models.CharField(max_length=15)  # TODO check if this is correct
    ping = models.IntegerField()
    index = models.IntegerField()
    state = models.CharField(max_length=30)  # TODO this is ugly
    join_time = models.IntegerField()
    host = models.BooleanField()


class Participant(models.Model):
    member = models.ForeignKey(Member)
    # TODO status = active, left

    ingame_id = models.IntegerField()
    refid = models.IntegerField()
    name = models.CharField(max_length=200)
    is_ai = models.BooleanField()
    vehicle = models.ForeignKey(Vehicle)
    livery = models.ForeignKey(Livery)


class ParticipantSnapshot(models.Model):
    participant = models.ForeignKey(Participant)
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


class Event(models.Model):
    snapshot = models.ForeignKey(SessionSnapshot, null=True)
    definition = models.ForeignKey(EventDefinition, null=True)  # may be NULL and a custom event! eg. by a plugin
    session = models.ForeignKey(SessionSnapshot)


class RaceLapSnapshot(models.Model):
    snapshot = models.ForeignKey(SessionSnapshot, null=True)
    session = models.ForeignKey(SessionSnapshot)
    lap = models.IntegerField()


class Lap(models.Model):
    session = models.ForeignKey(SessionSnapshot)
    participant = models.ForeignKey(Participant)
    lap = models.IntegerField()
    count_this_lap = models.BooleanField()
    lap_time_seconds = models.IntegerField()
    position = models.IntegerField()
    sector1_time = models.IntegerField()
    sector2_time = models.IntegerField()
    sector3_time = models.IntegerField()
    distance_travelled = models.IntegerField()


class Sector(models.Model):
    session = models.ForeignKey(SessionSnapshot)
    participant = models.ForeignKey(Participant)
    lap = models.ForeignKey(Lap)
    count_this_lap = models.BooleanField()
    sector = models.SmallIntegerField()
    sector_time = models.IntegerField()