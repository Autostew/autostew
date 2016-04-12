from autostew_web_enums.models import SessionFlagDefinition, DamageDefinition, TireWearDefinition, FuelUsageDefinition, \
    PenaltyDefinition, AllowedViewsDefinition, WeatherDefinition, GameModeDefinition, SessionState, SessionStage, \
    SessionPhase, PrivacyDefinition
from autostew_web_session.models.models import Track, VehicleClass, Vehicle

session_setup_translations = [
    {'model_field': 'server_controls_setup', 'api_field': 'ServerControlsSetup'},
    {'model_field': 'server_controls_track', 'api_field': 'ServerControlsTrack'},
    {'model_field': 'server_controls_vehicle_class', 'api_field': 'ServerControlsVehicleClass'},
    {'model_field': 'server_controls_vehicle', 'api_field': 'ServerControlsVehicle'},
    {'model_field': 'grid_size', 'api_field': 'GridSize'},
    {'model_field': 'max_players', 'api_field': 'MaxPlayers'},
    {'model_field': 'opponent_difficulty', 'api_field': 'OpponentDifficulty'},

    {'model_field': 'force_identical_vehicles', 'flag': SessionFlagDefinition.force_identical_vehicles, 'api_field': 'Flags'},
    {'model_field': 'allow_custom_vehicle_setup', 'flag': SessionFlagDefinition.allow_custom_vehicle_setup, 'api_field': 'Flags'},
    {'model_field': 'force_realistic_driving_aids', 'flag': SessionFlagDefinition.force_realistic_driving_aids, 'api_field': 'Flags'},
    {'model_field': 'abs_allowed', 'flag': SessionFlagDefinition.abs_allowed, 'api_field': 'Flags'},
    {'model_field': 'sc_allowed', 'flag': SessionFlagDefinition.sc_allowed, 'api_field': 'Flags'},
    {'model_field': 'tcs_allowed', 'flag': SessionFlagDefinition.tcs_allowed, 'api_field': 'Flags'},
    {'model_field': 'force_manual', 'flag': SessionFlagDefinition.force_manual, 'api_field': 'Flags'},
    {'model_field': 'rolling_starts', 'flag': SessionFlagDefinition.rolling_starts, 'api_field': 'Flags'},
    {'model_field': 'force_same_vehicle_class', 'flag': SessionFlagDefinition.force_same_vehicle_class, 'api_field': 'Flags'},
    {'model_field': 'fill_session_with_ai', 'flag': SessionFlagDefinition.fill_session_with_ai, 'api_field': 'Flags'},
    {'model_field': 'mechanical_failures', 'flag': SessionFlagDefinition.mechanical_failures, 'api_field': 'Flags'},
    {'model_field': 'auto_start_engine', 'flag': SessionFlagDefinition.auto_start_engine, 'api_field': 'Flags'},
    {'model_field': 'timed_race', 'flag': SessionFlagDefinition.timed_race, 'api_field': 'Flags'},
    {'model_field': 'ghost_griefers', 'flag': SessionFlagDefinition.ghost_griefers, 'api_field': 'Flags'},
    {'model_field': 'enforced_pitstop', 'flag': SessionFlagDefinition.enforced_pitstop, 'api_field': 'Flags'},

    {'model_field': 'practice1_length', 'api_field': 'Practice1Length'},
    {'model_field': 'practice2_length', 'api_field': 'Practice2Length'},
    {'model_field': 'qualify_length', 'api_field': 'QualifyLength'},
    {'model_field': 'warmup_length', 'api_field': 'WarmupLength'},
    {'model_field': 'race1_length', 'api_field': 'Race1Length'},
    {'model_field': 'race2_length', 'api_field': 'Race2Length'},

    {'model_field': 'privacy', 'api_field': 'Privacy', 'enum_model': PrivacyDefinition},
    {'model_field': 'damage', 'api_field': 'DamageType', 'enum_model': DamageDefinition},
    {'model_field': 'tire_wear', 'api_field': 'TireWearType', 'enum_model': TireWearDefinition},
    {'model_field': 'fuel_usage', 'api_field': 'FuelUsageType', 'enum_model': FuelUsageDefinition},
    {'model_field': 'penalties', 'api_field': 'PenaltiesType', 'enum_model': PenaltyDefinition},
    {'model_field': 'allowed_views', 'api_field': 'AllowedViews', 'enum_model': AllowedViewsDefinition},
    {'model_field': 'track', 'api_field': 'TrackId', 'enum_model': Track},
    {'model_field': 'vehicle_class', 'api_field': 'VehicleClassId', 'enum_model': VehicleClass},
    {'model_field': 'vehicle', 'api_field': 'VehicleModelId', 'enum_model': Vehicle},

    {'model_field': 'date_year', 'api_field': 'DateYear'},
    {'model_field': 'date_month', 'api_field': 'DateMonth'},
    {'model_field': 'date_day', 'api_field': 'DateDay'},
    {'model_field': 'date_hour', 'api_field': 'DateHour'},
    {'model_field': 'date_minute', 'api_field': 'DateMinute'},
    {'model_field': 'date_progression', 'api_field': 'DateProgression'},
    {'model_field': 'weather_progression', 'api_field': 'ForecastProgression'},
    {'model_field': 'weather_slots', 'api_field': 'WeatherSlots'},

    {'model_field': 'weather_1', 'api_field': 'WeatherSlot1', 'enum_model': WeatherDefinition},
    {'model_field': 'weather_2', 'api_field': 'WeatherSlot2', 'enum_model': WeatherDefinition},
    {'model_field': 'weather_3', 'api_field': 'WeatherSlot3', 'enum_model': WeatherDefinition},
    {'model_field': 'weather_4', 'api_field': 'WeatherSlot4', 'enum_model': WeatherDefinition},

    {'model_field': 'game_mode', 'api_field': 'GameMode', 'enum_model': GameModeDefinition},
]

extra_track_data_translations = [
    {'model_field': 'track_latitude', 'api_field': 'Latitude'},
    {'model_field': 'track_longitude', 'api_field': 'Longitude'},
    {'model_field': 'track_altitude', 'api_field': 'Altitude'},
]

session_translations = [
    {'model_field': 'session_state', 'api_field': 'SessionState', 'enum_model': SessionState},
    {'model_field': 'session_stage', 'api_field': 'SessionStage', 'enum_model': SessionStage},
    {'model_field': 'session_phase', 'api_field': 'SessionPhase', 'enum_model': SessionPhase},
    {'model_field': 'session_time_elapsed', 'api_field': 'SessionTimeElapsed'},
    {'model_field': 'session_time_duration', 'api_field': 'SessionTimeDuration'},
    {'model_field': 'num_participants_valid', 'api_field': 'NumParticipantsValid'},
    {'model_field': 'num_participants_disq', 'api_field': 'NumParticipantsDisqualified'},
    {'model_field': 'num_participants_retired', 'api_field': 'NumParticipantsRetired'},
    {'model_field': 'num_participants_dnf', 'api_field': 'NumParticipantsDNF'},
    {'model_field': 'num_participants_finished', 'api_field': 'NumParticipantsFinished'},
    {'model_field': 'current_year', 'api_field': 'CurrentYear'},
    {'model_field': 'current_month', 'api_field': 'CurrentMonth'},
    {'model_field': 'current_day', 'api_field': 'CurrentDay'},
    {'model_field': 'current_hour', 'api_field': 'CurrentHour'},
    {'model_field': 'current_minute', 'api_field': 'CurrentMinute'},
    {'model_field': 'rain_density_visual', 'api_field': 'RainDensity'},
    {'model_field': 'wetness_path', 'api_field': 'WetnessOnPath'},
    {'model_field': 'wetness_off_path', 'api_field': 'WetnessOffPath'},
    {'model_field': 'wetness_avg', 'api_field': 'WetnessAverage'},
    {'model_field': 'wetness_predicted_max', 'api_field': 'WetnessPredictedMax'},
    {'model_field': 'wetness_max_level', 'api_field': 'WetnessMaxLevel'},
    {'model_field': 'temperature_ambient', 'api_field': 'TemperatureAmbient'},
    {'model_field': 'temperature_track', 'api_field': 'TemperatureTrack'},
    {'model_field': 'air_pressure', 'api_field': 'AirPressure'},
]
