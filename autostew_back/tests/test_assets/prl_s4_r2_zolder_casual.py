from autostew_web_enums.models import PrivacyDefinition
from autostew_web_session.models.session import SessionSetup

name = 'Good morning at Zolder'

def make_setup(server):
    server.session_api.privacy.set_to_game(PrivacyDefinition.public)
    server.session_api.server_controls_setup.set_to_game(1)
    server.session_api.server_controls_track.set_to_game(1)
    server.session_api.server_controls_vehicle_class.set_to_game(1)
    server.session_api.server_controls_vehicle.set_to_game(0)

    server.session_api.vehicle_class.set_to_game_nice('GT3')
    server.session_api.track.set_to_game_nice("Zolder")
    server.session_api.grid_size.set_to_game(22, for_next_session=True)
    server.session_api.max_players.set_to_game(8)

    server.session_api.weather_slots.set_to_game(1)
    # server.session_api.weather_progression.set_to_game(5)
    server.session_api.weather_1.set_to_game_nice("Clear")

    server.session_api.flags.set_flags([
        SessionSetup.abs_allowed,
        SessionSetup.force_identical_vehicles,
        SessionSetup.force_manual,
        SessionSetup.mechanical_failures,
        SessionSetup.rolling_starts,
        SessionSetup.sc_allowed,
        SessionSetup.tcs_allowed,
        SessionSetup.timed_race
    ], 0)
    server.session_api.flags.set_flags([
        SessionSetup.allow_custom_vehicle_setup,
        SessionSetup.auto_start_engine,
        SessionSetup.enforced_pitstop,
        SessionSetup.fill_session_with_ai,
        SessionSetup.force_realistic_driving_aids,
        SessionSetup.force_same_vehicle_class,
        SessionSetup.ghost_griefers,
    ], 1)

    server.session_api.tire_wear.set_to_game_nice("X2")
    server.session_api.allowed_views.set_to_game_nice('Any')
    server.session_api.damage.set_to_game_nice('FULL')
    server.session_api.fuel_usage.set_to_game_nice('STANDARD')
    server.session_api.opponent_difficulty.set_to_game(100)
    server.session_api.penalties.set_to_game_nice('FULL')

    server.session_api.date_hour.set_to_game(13)
    server.session_api.date_minute.set_to_game(0)
    server.session_api.date_progression.set_to_game(5)

    server.session_api.practice1_length.set_to_game(0)
    server.session_api.practice2_length.set_to_game(0)
    server.session_api.qualify_length.set_to_game(10)
    server.session_api.warmup_length.set_to_game(0)
    server.session_api.race1_length.set_to_game(5)
