from autostew_back.gameserver.session import Privacy
from autostew_web_session.models.session_enums import SessionFlags, Privacy

name = 'Stint at home'

def make_setup(server):
    server.session_api.privacy.set_to_game(Privacy.public)
    server.session_api.server_controls_setup.set_to_game(1)
    server.session_api.server_controls_track.set_to_game(1)
    server.session_api.server_controls_vehicle_class.set_to_game(1)
    server.session_api.server_controls_vehicle.set_to_game(0)

    server.session_api.vehicle_class.set_to_game_nice('GT3')
    server.session_api.track.set_to_game_nice("Circuit de Barcelona-Catalunya GP")
    server.session_api.grid_size.set_to_game(30, for_next_session=True)
    server.session_api.max_players.set_to_game(24)

    server.session_api.weather_slots.set_to_game(2)
    server.session_api.weather_progression.set_to_game(5)
    server.session_api.weather_1.set_to_game_nice("LightCloud")
    server.session_api.weather_2.set_to_game_nice("Clear")

    server.session_api.flags.set_flags([
        SessionFlags.abs_allowed,
        SessionFlags.force_identical_vehicles,
        SessionFlags.force_manual,
        SessionFlags.mechanical_failures,
        SessionFlags.rolling_starts,
        SessionFlags.sc_allowed,
        SessionFlags.tcs_allowed,
        SessionFlags.timed_race,
    ], 0)
    server.session_api.flags.set_flags([
        SessionFlags.allow_custom_vehicle_setup,
        SessionFlags.auto_start_engine,
        SessionFlags.enforced_pitstop,
        SessionFlags.force_realistic_driving_aids,
        SessionFlags.force_same_vehicle_class,
        SessionFlags.ghost_griefers,
        SessionFlags.fill_session_with_ai,
    ], 1)

    server.session_api.tire_wear.set_to_game_nice("STANDARD")
    server.session_api.allowed_views.set_to_game_nice('Any')
    server.session_api.damage.set_to_game_nice('FULL')
    server.session_api.fuel_usage.set_to_game_nice('STANDARD')
    server.session_api.opponent_difficulty.set_to_game(100)
    server.session_api.penalties.set_to_game_nice('FULL')

    server.session_api.date_hour.set_to_game(11)
    server.session_api.date_minute.set_to_game(0)
    server.session_api.date_progression.set_to_game(5)

    server.session_api.practice1_length.set_to_game(0)
    server.session_api.practice2_length.set_to_game(0)
    server.session_api.qualify_length.set_to_game(15)
    server.session_api.warmup_length.set_to_game(0)
    server.session_api.race1_length.set_to_game(7)
