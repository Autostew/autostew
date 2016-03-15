import factory


class SessionSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'autostew_web_session.SessionSetup'

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
    damage = models.ForeignKey('autostew_web_enums.DamageDefinition', null=True)
    tire_wear = models.ForeignKey('autostew_web_enums.TireWearDefinition', null=True)
    fuel_usage = models.ForeignKey('autostew_web_enums.FuelUsageDefinition', null=True)
    penalties = models.ForeignKey('autostew_web_enums.PenaltyDefinition', null=True)
    allowed_views = models.ForeignKey('autostew_web_enums.AllowedViewsDefinition', null=True)
    track = models.ForeignKey(Track, null=True)
    vehicle_class = models.ForeignKey(VehicleClass, null=True)
    vehicle = models.ForeignKey(Vehicle, null=True)
    date_year = 0
    date_month = 0
    date_day = 0
    date_hour = 0
    date_minute = 0
    date_progression = 0
    weather_progression = 0
    weather_slots = 0
    weather_1 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True)
    weather_2 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True)
    weather_3 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True)
    weather_4 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True)
    game_mode = models.ForeignKey('autostew_web_enums.GameModeDefinition', related_name='+', null=True)
    track_latitude = 0
    track_longitude = 0
    track_altitude = 0
