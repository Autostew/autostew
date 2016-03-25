from autostew_back.gameserver.session import Privacy, SessionFlags

name = 'Precision Racing League Season 4 Round 3 - Hockenheim GP'

def make_setup(server):
    server.session.privacy.set_to_game(Privacy.public)
    server.session.server_controls_setup.set_to_game(1)
    server.session.server_controls_track.set_to_game(1)
    server.session.server_controls_vehicle_class.set_to_game(1)
    server.session.server_controls_vehicle.set_to_game(0)

    server.session.vehicle_class.set_to_game_nice('TC1')
    server.session.track.set_to_game_nice("Dubai Autodrome National")
    server.session.grid_size.set_to_game(24, for_next_session=True)
    server.session.max_players.set_to_game(24)

    server.session.weather_slots.set_to_game(0)
    server.session.weather_progression.set_to_game(1)

    server.session.flags.set_flags([
        SessionFlags.abs_allowed,
        SessionFlags.force_identical_vehicles,
        SessionFlags.force_manual,
        SessionFlags.mechanical_failures,
        SessionFlags.rolling_starts,
        SessionFlags.sc_allowed,
        SessionFlags.tcs_allowed,
        SessionFlags.fill_session_with_ai,
        SessionFlags.timed_race
    ], 0)
    server.session.flags.set_flags([
        SessionFlags.allow_custom_vehicle_setup,
        SessionFlags.auto_start_engine,
        SessionFlags.enforced_pitstop,
        SessionFlags.force_realistic_driving_aids,
        SessionFlags.force_same_vehicle_class,
        SessionFlags.ghost_griefers,
    ], 1)

    server.session.tire_wear.set_to_game_nice("X3")
    server.session.allowed_views.set_to_game_nice('Any')
    server.session.damage.set_to_game_nice('FULL')
    server.session.fuel_usage.set_to_game_nice('STANDARD')
    server.session.opponent_difficulty.set_to_game(100)
    server.session.penalties.set_to_game_nice('FULL')

    server.session.date_hour.set_to_game(21)
    server.session.date_minute.set_to_game(0)
    server.session.date_progression.set_to_game(1)

    server.session.practice1_length.set_to_game(45)
    server.session.practice2_length.set_to_game(0)
    server.session.qualify_length.set_to_game(15)
    server.session.warmup_length.set_to_game(5)
    server.session.race1_length.set_to_game(25)