import factory

from autostew_web_session.models.models import SessionSetup
from autostew_web_session.tests.factories.enum_factories import *


class SessionSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SessionSetup

    server_controls_setup = False
    server_controls_track = False
    server_controls_vehicle_class = False
    server_controls_vehicle = False
    grid_size = 0
    max_players = 0
    opponent_difficulty = 0

    force_identical_vehicles = False
    allow_custom_vehicle_setup = False
    force_realistic_driving_aids = False
    abs_allowed = False
    sc_allowed = False
    tcs_allowed = False
    force_manual = False
    rolling_starts = False
    force_same_vehicle_class = False
    fill_session_with_ai = False
    mechanical_failures = False
    auto_start_engine = False
    timed_race = False
    ghost_griefers = False
    enforced_pitstop = False

    practice1_length = 0
    practice2_length = 0
    qualify_length = 0
    warmup_length = 0
    race1_length = 0
    race2_length = 0

    public = False
    friends_can_join = False
    damage = factory.SubFactory(DamageFactory)
    tire_wear = factory.SubFactory(TireWearFactory)
    fuel_usage = factory.SubFactory(FuelUsageFactory)
    penalties = factory.SubFactory(PenaltyFactory)
    allowed_views = factory.SubFactory(AllowedViewsFactory)
    track = None
    vehicle_class = None
    vehicle = None
    date_year = 0
    date_month = 0
    date_day = 0
    date_hour = 0
    date_minute = 0
    date_progression = 0
    weather_progression = 0
    weather_slots = 0
    weather_1 = factory.SubFactory(WeatherFactory)
    weather_2 = factory.SubFactory(WeatherFactory)
    weather_3 = factory.SubFactory(WeatherFactory)
    weather_4 = factory.SubFactory(WeatherFactory)
    game_mode = factory.SubFactory(WeatherFactory)
    track_latitude = 0
    track_longitude = 0
    track_altitude = 0
