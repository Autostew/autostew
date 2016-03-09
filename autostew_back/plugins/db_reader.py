from autostew_back.gameserver.session import Privacy, SessionFlags
from autostew_back.plugins import db
from autostew_web_session.models import Server, SessionSetup

name = 'DB reader'
dependencies = [db]

server_in_db = None


def init(server):
    global server_in_db

    server.settings.setup_rotation = [DBSetup(setup) for setup in load_settings()]

    try:
        server_in_db = Server.objects.get(name=server.settings.server_name)
    except Server.DoesNotExist:
        server_in_db = Server(name=server.settings.server_name, running=True)

    # TODO load plugins from server
    # and then raise BreakPluginLoadingException


class DBSetup:
    def __init__(self, setup: SessionSetup):
        self.setup = setup

    def make_setup(self, server):
        server.session.privacy.set_to_game(Privacy.public if self.setup.public else
                                           Privacy.friends if self.setup.friends_can_join else
                                           Privacy.private)
        server.session.server_controls_setup.set_to_game(self.setup.server_controls_setup)
        server.session.server_controls_track.set_to_game(self.setup.server_controls_track)
        server.session.server_controls_vehicle_class.set_to_game(self.setup.server_controls_vehicle_class)
        server.session.server_controls_vehicle.set_to_game(self.setup.server_controls_vehicle)

        server.session.vehicle_class.set_to_game(self.setup.vehicle_class.ingame_id)
        server.session.track.set_to_game(self.setup.track.ingame_id)
        server.session.grid_size.set_to_game(self.setup.grid_size)
        server.session.max_players.set_to_game(self.setup.max_players)

        server.session.weather_slots.set_to_game(self.setup.weather_slots)
        server.session.weather_progression.set_to_game(self.setup.weather_progression)
        server.session.weather_1.set_to_game(self.setup.weather_1.ingame_id)
        server.session.weather_2.set_to_game(self.setup.weather_2.ingame_id)
        server.session.weather_3.set_to_game(self.setup.weather_3.ingame_id)
        server.session.weather_4.set_to_game(self.setup.weather_4.ingame_id)

        server.session.flags.set_flags(SessionFlags.abs_allowed, self.setup.abs_allowed)

        server.session.flags.set_flags(SessionFlags.force_identical_vehicles, self.setup.force_identical_vehicles)
        server.session.flags.set_flags(SessionFlags.force_manual, self.setup.force_manual)
        server.session.flags.set_flags(SessionFlags.mechanical_failures, self.setup.mechanical_failures)
        server.session.flags.set_flags(SessionFlags.rolling_starts, self.setup.rolling_starts)
        server.session.flags.set_flags(SessionFlags.sc_allowed, self.setup.sc_allowed)
        server.session.flags.set_flags(SessionFlags.tcs_allowed, self.setup.tcs_allowed)
        server.session.flags.set_flags(SessionFlags.timed_race, self.setup.timed_race)
        server.session.flags.set_flags(SessionFlags.allow_custom_vehicle_setup, self.setup.allow_custom_vehicle_setup)
        server.session.flags.set_flags(SessionFlags.auto_start_engine, self.setup.auto_start_engine)
        server.session.flags.set_flags(SessionFlags.enforced_pitstop, self.setup.enforced_pitstop)
        server.session.flags.set_flags(SessionFlags.fill_session_with_ai, self.setup.fill_session_with_ai)
        server.session.flags.set_flags(SessionFlags.force_realistic_driving_aids, self.setup.force_realistic_driving_aids)
        server.session.flags.set_flags(SessionFlags.force_same_vehicle_class, self.setup.force_same_vehicle_class)
        server.session.flags.set_flags(SessionFlags.ghost_griefers, self.setup.ghost_griefers)

        server.session.tire_wear.set_to_game_nice("X2")
        server.session.allowed_views.set_to_game_nice('Any')
        server.session.damage.set_to_game_nice('FULL')
        server.session.fuel_usage.set_to_game_nice('STANDARD')
        server.session.opponent_difficulty.set_to_game(100)
        server.session.penalties.set_to_game_nice('FULL')

        server.session.date_hour.set_to_game(11)
        server.session.date_minute.set_to_game(0)
        server.session.date_progression.set_to_game(5)

        server.session.practice1_length.set_to_game(45)
        server.session.practice2_length.set_to_game(0)
        server.session.qualify_length.set_to_game(15)
        server.session.warmup_length.set_to_game(5)
        server.session.race1_length.set_to_game(25)


def event(server, event):
    pass


def load_settings():
    return SessionSetup.objects.all()


def tick(server):
    pass

