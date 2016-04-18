from django.db import models


class EventDefinition(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    attributes = models.TextField(max_length=200)

    def __str__(self):
        return "{}-{}".format(self.type, self.name)

    @classmethod
    def get_or_create_default(cls, name):
        return cls.objects.get_or_create(name=name, defaults={'type': 'Unknown', 'decription': '', 'attributes': ''})[0]


class GameModeDefinition(models.Model):
    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class TireWearDefinition(models.Model):
    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class PenaltyDefinition(models.Model):
    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class FuelUsageDefinition(models.Model):
    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class AllowedViewsDefinition(models.Model):
    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class PlayerFlagDefinition(models.Model):
    setup_used = 1
    controller_gamepad = 2
    controller_wheel = 4
    controller_mask = 6
    aid_steering = 8
    aid_braking = 16
    aid_abs = 32
    aid_traction = 64
    aid_stability = 128
    aid_no_damage = 256
    aid_auto_gears = 512
    aid_auto_clutch = 1024
    model_normal = 2048
    model_experienced = 4096
    model_pro = 6144
    model_elite = 8192
    model_mask = 14336
    aid_driving_line = 32768
    valid = 1073741824

    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class WeatherDefinition(models.Model):
    name_to_icon = {
        'Random': '<span class="glyphicon glyphicon-question-sign" aria-hidden="true" title="{}"></span>',
        'Hazy': '<i class="wi wi-day-haze" title="{}"></i>',
        'HeavyFogWithRain': '<i class="wi wi-rain-wind" title="{}"></i>',
        'FogWithRain': '<i class="wi wi-day-rain-wind" title="{}"></i>',
        'HeavyFog': '<i class="wi wi-fog" title="{}"></i>',
        'Foggy': '<i class="wi wi-day-fog" title="{}"></i>',
        'ThunderStorm': '<i class="wi wi-thunderstorm" title="{}"></i>',
        'Storm': '<i class="wi wi-day-storm-showers" title="{}"></i>',
        'Rain': '<i class="wi wi-day-rain" title="{}"></i>',
        'LightRain': '<i class="wi wi-day-sleet" title="{}"></i>',
        'Overcast': '<i class="wi wi-day-cloudy-high" title="{}"></i>',
        'HeavyCloud': '<i class="wi wi-cloudy" title="{}"></i>',
        'MediumCloud': '<i class="wi wi-cloud" title="{}"></i>',
        'LightCloud': '<i class="wi wi-day-sunny-overcast" title="{}"></i>',
        'Clear': '<i class="wi wi-day-sunny" title="{}"></i>',
    }
    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def get_icon_or_name(self):
        return WeatherDefinition.name_to_icon.get(self.name, self.name).format(self.name)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class PrivacyDefinition(models.Model):
    public = 0
    friends = 1
    private = 2

    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class DamageDefinition(models.Model):
    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class SessionFlagDefinition(models.Model):
    force_identical_vehicles = 2
    allow_custom_vehicle_setup = 8
    force_realistic_driving_aids = 16
    abs_allowed = 32
    sc_allowed = 64
    tcs_allowed = 128
    force_manual = 256
    rolling_starts = 512
    force_same_vehicle_class = 1024
    fill_session_with_ai = 131072
    mechanical_failures = 262144
    auto_start_engine = 524288
    timed_race = 1048576
    ghost_griefers = 2097152
    enforced_pitstop = 4194304

    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


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


class EventType(models.Model):
    session_setup = 'SessionSetup'
    state_changed = 'StateChanged'
    stage_changed = 'StageChanged'
    session_created = 'SessionCreated'
    session_destroyed = 'SessionDestroyed'
    participant_state = 'State'
    server_chat = 'ServerChat'
    player_chat = 'PlayerChat'
    player_joined = 'PlayerJoined'
    authenticated = 'Authenticated'
    player_left = 'PlayerLeft'
    participant_created = 'ParticipantCreated'
    participant_destroyed = 'ParticipantDestroyed'
    sector = 'Sector'
    lap = 'Lap'
    results = 'Results'
    cut_track_start = 'CutTrackStart'
    cut_track_end = 'CutTrackEnd'
    impact = 'Impact'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, name):
        return cls.objects.get_or_create(name=name)[0]


class LeavingReason(models.Model):
    left = 1
    kicked = 2
    disconnected = 5

    ingame_id = models.IntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class MemberLoadState(models.Model):
    admin_started_race = 'ADMIN_STARTED_RACE'
    admin_loading_race = 'ADMIN_LOADING_RACE'
    client_loading_race = 'CLIENT_LOADING_RACE'
    client_ready = 'CLIENT_READY'
    unknown = 'UNKNOWN'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, name):
        return cls.objects.get_or_create(name=name)[0]


class MemberState(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, name):
        return cls.objects.get_or_create(name=name)[0]


class ParticipantState(models.Model):
    none = ''
    racing = 'Racing'
    finished = 'Finished'
    dnf = 'DNF'
    disqualified = 'Disqualified'
    retired = 'Retired'
    in_garage = 'InGarage'
    entering_pits = 'EnteringPits'
    in_pits = 'InPits'
    exiting_pits = 'ExitingPits'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def in_race(self):
        return self.name not in ('DNF', 'Retired', 'Disqualified')

    @classmethod
    def get_or_create_default(cls, name):
        return cls.objects.get_or_create(name=name)[0]


class SessionState(models.Model):
    none = 'None'
    lobby = 'Lobby'
    loading = 'Loading'
    race = 'Race'
    post_race = 'PostRace'
    returning = 'Returning'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, name):
        return cls.objects.get_or_create(name=name)[0]


class SessionStage(models.Model):
    practice1 = 'Practice1'
    practice2 = 'Practice2'
    qualifying = 'Qualifying'
    warmup = 'Warmup'
    formationlap = 'FormationLap'
    race1 = 'Race1'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def is_relevant(self):
        return self.name in ("Race", "Race1", "Race2", "Qualifying")

    @classmethod
    def get_or_create_default(cls, name):
        return cls.objects.get_or_create(name=name)[0]


class SessionPhase(models.Model):
    pre_countdown_sync = 'PreCountDownSync'
    prerace = 'PreRace'
    countdown_wait = 'CountDownWait'
    countdown = 'CountDown'
    green = 'Green'
    invalid = 'Invalid'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, name):
        return cls.objects.get_or_create(name=name)[0]

