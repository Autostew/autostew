import datetime
import logging

from django.utils import timezone

from autostew_back.gameserver.event import EventType
from autostew_back.gameserver.server import Server
from autostew_back.gameserver.session import Privacy, SessionFlags, SessionState
from autostew_back.plugins import db
from autostew_web_session.models import SessionSetup

name = 'DB setup rotation'
dependencies = [db]

setup_rotation = []
scheduled_session = None
current_setup = None
_setup_index = None


class NoSessionSetupTemplateAvailable(Exception):
    pass


def init(server: Server):
    global setup_rotation
    server.get_current_setup_name = get_current_setup_name
    load_settings(server)
    load_next_setup(server)


def event(server, event):
    global setup_rotation
    if event.type == EventType.state_changed:
        if event.new_state == SessionState.lobby:
            load_settings(server)
            load_next_setup(server)


def load_settings(server):
    global setup_rotation
    global scheduled_session
    for scheduled_session_it in db.server_in_db.scheduled_sessions.all():
        if (
                not scheduled_session_it.running and not scheduled_session_it.finished
                (not scheduled_session_it.schedule_date or scheduled_session_it.schedule_date == datetime.date.today())
                and abs(scheduled_session_it.schedule_time - datetime.time()) < datetime.timedelta(seconds=300)
        ):
            scheduled_session = scheduled_session_it
            return
    if db.server_in_db.next_setup:
        setup_rotation = [db.server_in_db.next_setup]
        db.server_in_db.next_setup = None
        db.server_in_db.save()
    else:
        setup_rotation = [
            DBSetup(setup) for setup in db.server_in_db.session_setups.all()
        ]


def load_next_setup(server: Server, force_index=None):
    global _setup_index
    global current_setup
    if scheduled_session:
        current_setup = DBSetup(scheduled_session.setup_template)
    else:
        if force_index is None:
            load_index = 0 if _setup_index is None else _setup_index + 1
        else:
            load_index = force_index
        if load_index >= len(setup_rotation):
            load_index = 0
        if len(setup_rotation) == 0:
            raise NoSessionSetupTemplateAvailable
        _setup_index = load_index
        current_setup = setup_rotation[load_index]
    logging.info("Loading setup {}: {}".format(load_index, current_setup.name))
    current_setup.make_setup(server)


def get_current_setup_name():
    return current_setup.name


class DBSetup:
    def __init__(self, setup: SessionSetup):
        self.setup = setup
        self.name = setup.name

    def make_setup(self, server: Server):
        server.session.privacy.set_to_game(Privacy.public if self.setup.public else
                                           Privacy.friends if self.setup.friends_can_join else
                                           Privacy.private)
        server.session.server_controls_setup.set_to_game(self.setup.server_controls_setup)
        server.session.server_controls_track.set_to_game(self.setup.server_controls_track)
        server.session.server_controls_vehicle_class.set_to_game(self.setup.server_controls_vehicle_class)
        server.session.server_controls_vehicle.set_to_game(self.setup.server_controls_vehicle)

        if self.setup.vehicle_class:
            server.session.vehicle_class.set_to_game(self.setup.vehicle_class.ingame_id)
        if self.setup.track:
            server.session.track.set_to_game(self.setup.track.ingame_id)
        server.session.grid_size.set_to_game(self.setup.grid_size)
        server.session.max_players.set_to_game(self.setup.max_players)

        server.session.weather_slots.set_to_game(self.setup.weather_slots)
        server.session.weather_progression.set_to_game(self.setup.weather_progression)
        if self.setup.weather_1:
            server.session.weather_1.set_to_game(self.setup.weather_1.ingame_id)
        if self.setup.weather_2:
            server.session.weather_2.set_to_game(self.setup.weather_2.ingame_id)
        if self.setup.weather_3:
            server.session.weather_3.set_to_game(self.setup.weather_3.ingame_id)
        if self.setup.weather_4:
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

        server.session.tire_wear.set_to_game(self.setup.tire_wear.ingame_id)
        server.session.allowed_views.set_to_game(self.setup.allowed_views.ingame_id)
        server.session.damage.set_to_game(self.setup.damage.ingame_id)
        server.session.fuel_usage.set_to_game(self.setup.fuel_usage.ingame_id)
        server.session.opponent_difficulty.set_to_game(100)
        server.session.penalties.set_to_game(self.setup.penalties.ingame_id)

        server.session.date_hour.set_to_game(self.setup.date_hour)
        server.session.date_minute.set_to_game(self.setup.date_minute)
        server.session.date_progression.set_to_game(self.setup.date_progression)

        server.session.practice1_length.set_to_game(self.setup.practice1_length)
        server.session.practice2_length.set_to_game(self.setup.practice2_length)
        server.session.qualify_length.set_to_game(self.setup.qualify_length)
        server.session.warmup_length.set_to_game(self.setup.warmup_length)
        server.session.race1_length.set_to_game(self.setup.race1_length)
        server.session.race2_length.set_to_game(self.setup.race2_length)
        server.fetch_status()

