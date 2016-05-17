from autostew_web_enums.factories.enum_factories import *
from autostew_web_session.models.session import SessionSetup


class SessionSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SessionSetup

    name = factory.Sequence(lambda n: 'SessionSetup%d' % n)
    is_template = False

    server_controls_setup = False
    server_controls_track = False
    server_controls_vehicle_class = False
    server_controls_vehicle = False
    grid_size = 32
    max_players = 32
    opponent_difficulty = 100

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
    race1_length = 5
    race2_length = 0

    privacy = factory.SubFactory(PrivacyDefinitionFactory)
    damage = factory.SubFactory(DamageDefinitionFactory)
    tire_wear = factory.SubFactory(TireWearDefinitionFactory)
    fuel_usage = factory.SubFactory(FuelUsageDefinitionFactory)
    penalties = factory.SubFactory(PenaltyDefinitionFactory)
    allowed_views = factory.SubFactory(AllowedViewsDefinitionFactory)
    track = None
    vehicle_class = None
    vehicle = None
    date_year = 0
    date_month = 0
    date_day = 0
    date_hour = 9
    date_minute = 0
    date_progression = 1
    weather_progression = 1
    weather_slots = 0
    weather_1 = None
    weather_2 = None
    weather_3 = None
    weather_4 = None
    game_mode = None
