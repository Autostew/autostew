from unittest import mock

import requests
from django.test import TestCase

import autostew_web_session.models.server
import autostew_web_session.models.session
from autostew_back.gameserver.mocked_api import FakeApi
from autostew_back.gameserver.participant import ParticipantState
from autostew_web_session.models.server import UnmetPluginDependencyException, Server
from autostew_back.tests.test_assets import settings_db_enum_writer, settings_db_session_writer
from autostew_web_enums.models import DamageDefinition, TireWearDefinition, FuelUsageDefinition, PenaltyDefinition, \
    AllowedViewsDefinition, WeatherDefinition, GameModeDefinition, PrivacyDefinition, MemberLoadState, MemberState
from autostew_web_session.models.models import Track, VehicleClass, Vehicle, SetupRotationEntry
from autostew_web_session.models.participant import Participant
from autostew_web_session.models.session import SessionSetup, Session
from autostew_web_session.models.member import Member


class TestDBWriter(TestCase):
    @classmethod
    def make_test_server(cls):
        return Server.objects.create(
            name="TestServer",
            running=False,
            setup_rotation_index=0,
            api_url='http://localhost:9000'
        )

    @classmethod
    def make_test_setup(cls) -> SessionSetup:
        cls.enum_defaults = defaults = {'ingame_id': 0}
        vehicle_class = VehicleClass.objects.get_or_create(name="GT3", defaults=cls.enum_defaults)[0]
        return SessionSetup(
            name='test',
            is_template=True,
            server_controls_setup=True,
            server_controls_track=True,
            server_controls_vehicle_class=True,
            server_controls_vehicle=True,
            grid_size=24,
            max_players=24,
            opponent_difficulty=100,
            force_identical_vehicles=False,
            allow_custom_vehicle_setup=True,
            force_realistic_driving_aids=True,
            abs_allowed=False,
            sc_allowed=False,
            tcs_allowed=False,
            force_manual=False,
            rolling_starts=False,
            force_same_vehicle_class=True,
            fill_session_with_ai=False,
            mechanical_failures=True,
            auto_start_engine=True,
            timed_race=False,
            ghost_griefers=True,
            enforced_pitstop=True,
            practice1_length=60,
            practice2_length=0,
            qualify_length=15,
            warmup_length=5,
            race1_length=25,
            race2_length=0,
            privacy=PrivacyDefinition.get_or_create_default(2),
            damage=DamageDefinition.objects.get_or_create(name="FULL", defaults=cls.enum_defaults)[0],
            tire_wear=TireWearDefinition.objects.get_or_create(name="X2", defaults=cls.enum_defaults)[0],
            fuel_usage=FuelUsageDefinition.objects.get_or_create(name="STANDARD", defaults=cls.enum_defaults)[0],
            penalties=PenaltyDefinition.objects.get_or_create(name="FULL", defaults=cls.enum_defaults)[0],
            allowed_views=AllowedViewsDefinition.objects.get_or_create(name="Any", defaults=cls.enum_defaults)[0],
            track=Track.objects.get_or_create(name="Hockenheim GP", defaults={'ingame_id': 1, 'grid_size': 24})[0],
            vehicle_class=vehicle_class,
            vehicle=Vehicle.objects.get_or_create(
                name="McLaren 12C GT3",
                vehicle_class=vehicle_class,
                defaults=cls.enum_defaults
            )[0],
            date_year=2016,
            date_month=1,
            date_day=1,
            date_hour=0,
            date_minute=0,
            date_progression=1,
            weather_progression=1,
            weather_slots=1,
            weather_1=WeatherDefinition.objects.get_or_create(name="Clear", defaults=cls.enum_defaults)[0],
            weather_2=WeatherDefinition.objects.get(name="Clear"),
            weather_3=WeatherDefinition.objects.get(name="Clear"),
            weather_4=WeatherDefinition.objects.get(name="Clear"),
            game_mode=GameModeDefinition.objects.get_or_create(name="MP_Race", defaults=cls.enum_defaults)[0],
        )

    def test_create_session_in_lobby(self):
        """
        Tests writing a basic session into the database
        """
        api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
        server = TestDBWriter.make_test_server()
        with mock.patch.object(requests, 'get', api.fake_request):
            server.back_start(settings_db_enum_writer, True)
        test_setup = self.make_test_setup()
        test_setup.save(True)
        SetupRotationEntry.objects.create(
            order=0,
            server=server,
            setup=test_setup
        )
        with mock.patch.object(requests, 'get', api.fake_request):
            server.back_start(settings_db_session_writer)
        self.assertEqual(autostew_web_session.models.server.Server.objects.count(), 1)
        self.assertEqual(SessionSetup.objects.count(), 2)
        self.assertEqual(Session.objects.filter(parent=None).count(), 1)
        self.assertEqual(Session.objects.count(), 2)
        self.assertEqual(Member.objects.filter(parent=None).count(), 1)
        self.assertEqual(Member.objects.count(), 2)
        self.assertEqual(Participant.objects.count(), 0)

        server_in_db = autostew_web_session.models.server.Server.objects.all()[0]
        self.assertTrue(server_in_db.running)

        session_setup = autostew_web_session.models.session.SessionSetup.objects.get(is_template=False)
        self.assertTrue(session_setup.server_controls_setup)
        self.assertTrue(session_setup.server_controls_track)
        self.assertFalse(session_setup.server_controls_vehicle)
        self.assertTrue(session_setup.server_controls_vehicle_class)
        self.assertEqual(session_setup.grid_size, 22)
        self.assertEqual(session_setup.max_players, 8)
        self.assertEqual(session_setup.opponent_difficulty, 100)
        self.assertEqual(session_setup.force_identical_vehicles, False)
        self.assertEqual(session_setup.allow_custom_vehicle_setup, True)
        self.assertEqual(session_setup.force_realistic_driving_aids, True)
        self.assertEqual(session_setup.force_manual, False)
        self.assertEqual(session_setup.rolling_starts, False)
        self.assertEqual(session_setup.force_same_vehicle_class, True)
        self.assertEqual(session_setup.fill_session_with_ai, True)
        self.assertEqual(session_setup.mechanical_failures, False)
        self.assertEqual(session_setup.auto_start_engine, True)
        self.assertEqual(session_setup.timed_race, False)
        self.assertEqual(session_setup.ghost_griefers, True)
        self.assertEqual(session_setup.enforced_pitstop, True)
        self.assertEqual(session_setup.practice1_length, 0)
        self.assertEqual(session_setup.practice2_length, 0)
        self.assertEqual(session_setup.qualify_length, 10)
        self.assertEqual(session_setup.warmup_length, 0)
        self.assertEqual(session_setup.race1_length, 5)
        self.assertEqual(session_setup.race2_length, 0)
        self.assertEqual(session_setup.public, True)
        self.assertEqual(session_setup.friends_can_join, True)
        self.assertEqual(session_setup.damage.name, "FULL")
        self.assertEqual(session_setup.tire_wear.name, "X2")
        self.assertEqual(session_setup.fuel_usage.name, "STANDARD")
        self.assertEqual(session_setup.penalties.name, "FULL")
        self.assertEqual(session_setup.allowed_views.name, "Any")
        self.assertEqual(session_setup.track.name, "Zolder")
        self.assertEqual(session_setup.vehicle_class.name, "GT3")
        self.assertEqual(session_setup.date_progression, 5)
        self.assertEqual(session_setup.weather_slots, 1)
        self.assertEqual(session_setup.weather_1.name, "Clear")

        session = Session.objects.all()[0]
        session_snapshot = Session.objects.filter(parent=None)[0]
        self.assertEqual(session.server, server_in_db)
        self.assertEqual(session.setup_actual, session_setup)
        self.assertEqual(session.planned, False)
        self.assertEqual(session.running, True)
        self.assertEqual(session.finished, False)
        self.assertEqual(session.lobby_id, '109775242847201392')
        self.assertEqual(session.max_member_count, 22)
        self.assertEqual(session.first_snapshot, session_snapshot)
        self.assertEqual(session.current_snapshot, session_snapshot)
        self.assertEqual(session.starting_snapshot_lobby, None)
        self.assertEqual(session.starting_snapshot_to_track, None)

        self.assertEqual(session_snapshot.session, session)
        self.assertEqual(session_snapshot.session_state.name, "Lobby")
        self.assertEqual(session_snapshot.session_stage.name, "Practice1")
        self.assertEqual(session_snapshot.session_phase.name, "Invalid")
        self.assertEqual(session_snapshot.session_time_elapsed, 0)
        self.assertEqual(session_snapshot.session_time_duration, 0)
        self.assertEqual(session_snapshot.num_participants_valid, 0)
        self.assertEqual(session_snapshot.num_participants_disq, 0)
        self.assertEqual(session_snapshot.num_participants_retired, 0)
        self.assertEqual(session_snapshot.num_participants_dnf, 0)
        self.assertEqual(session_snapshot.num_participants_finished, 0)
        self.assertEqual(session_snapshot.current_year, 2012)
        self.assertEqual(session_snapshot.current_month, 9)
        self.assertEqual(session_snapshot.current_day, 22)
        self.assertEqual(session_snapshot.current_hour, 6)
        self.assertEqual(session_snapshot.current_minute, 56)
        self.assertEqual(session_snapshot.rain_density_visual, 0)
        self.assertEqual(session_snapshot.wetness_path, 725)
        self.assertEqual(session_snapshot.wetness_off_path, 725)
        self.assertEqual(session_snapshot.wetness_avg, 725)
        self.assertEqual(session_snapshot.wetness_predicted_max, 0)
        self.assertEqual(session_snapshot.wetness_max_level, 725)
        self.assertEqual(session_snapshot.temperature_ambient, 21128)
        self.assertEqual(session_snapshot.temperature_track, 29692)
        self.assertEqual(session_snapshot.air_pressure, 101325)

        member = Member.objects.all()[0]
        self.assertEqual(member.session, session)
        self.assertEqual(member.still_connected, True)
        self.assertEqual(member.vehicle.name, "McLaren 12C GT3")
        self.assertEqual(member.livery.name, "McLaren #59")
        self.assertEqual(member.refid, 26752)
        self.assertEqual(member.steam_id, '76561197969382874')
        self.assertEqual(member.name, 'blak')
        # flags are not set, so they are not tested

        m_snap = Member.objects.exclude(parent=None)[0]
        self.assertEqual(m_snap.member, member)
        self.assertEqual(m_snap.snapshot, session_snapshot)
        self.assertEqual(m_snap.still_connected, True)
        self.assertEqual(m_snap.load_state.name, MemberLoadState.unknown)
        self.assertEqual(m_snap.ping, 10)
        self.assertEqual(m_snap.index, 0)
        self.assertEqual(m_snap.state.name, MemberState.connected)
        self.assertEqual(m_snap.host, True)

    def test_create_session_in_race(self):
        """
        Tests writing an in-qualifying session into the db
        """
        api = FakeApi('autostew_back/tests/test_assets/session_in_quali_two_players_14ai.json')
        server = TestDBWriter.make_test_server()
        with mock.patch.object(requests, 'get', api.fake_request):
            server.back_start(settings_db_enum_writer, True)
        test_setup = self.make_test_setup()
        test_setup.save(True)
        SetupRotationEntry.objects.create(
            order=0,
            server=server,
            setup=test_setup
        )
        with mock.patch.object(requests, 'get', api.fake_request):
            server.back_start(settings_db_session_writer)
        self.assertEqual(autostew_web_session.models.server.Server.objects.count(), 1)
        self.assertEqual(SessionSetup.objects.count(), 2)
        self.assertEqual(Session.objects.count(), 2)
        self.assertEqual(Member.objects.count(), 4)
        self.assertEqual(Participant.objects.count(), 32)

        server_in_db = autostew_web_session.models.server.Server.objects.all()[0]
        self.assertTrue(server_in_db.running)

        session_setup = autostew_web_session.models.session.SessionSetup.objects.get(is_template=False)
        self.assertTrue(session_setup.server_controls_setup)
        self.assertTrue(session_setup.server_controls_track)
        self.assertFalse(session_setup.server_controls_vehicle)
        self.assertTrue(session_setup.server_controls_vehicle_class)
        self.assertEqual(session_setup.grid_size, 22)
        self.assertEqual(session_setup.max_players, 8)
        self.assertEqual(session_setup.opponent_difficulty, 100)
        self.assertEqual(session_setup.force_identical_vehicles, False)
        self.assertEqual(session_setup.allow_custom_vehicle_setup, True)
        self.assertEqual(session_setup.force_realistic_driving_aids, True)
        self.assertEqual(session_setup.force_manual, False)
        self.assertEqual(session_setup.rolling_starts, False)
        self.assertEqual(session_setup.force_same_vehicle_class, True)
        self.assertEqual(session_setup.fill_session_with_ai, True)
        self.assertEqual(session_setup.mechanical_failures, False)
        self.assertEqual(session_setup.auto_start_engine, True)
        self.assertEqual(session_setup.timed_race, False)
        self.assertEqual(session_setup.ghost_griefers, True)
        self.assertEqual(session_setup.enforced_pitstop, True)
        self.assertEqual(session_setup.practice1_length, 0)
        self.assertEqual(session_setup.practice2_length, 0)
        self.assertEqual(session_setup.qualify_length, 10)
        self.assertEqual(session_setup.warmup_length, 0)
        self.assertEqual(session_setup.race1_length, 5)
        self.assertEqual(session_setup.race2_length, 0)
        self.assertEqual(session_setup.public, True)
        self.assertEqual(session_setup.friends_can_join, True)
        self.assertEqual(session_setup.damage.name, "FULL")
        self.assertEqual(session_setup.tire_wear.name, "X2")
        self.assertEqual(session_setup.fuel_usage.name, "STANDARD")
        self.assertEqual(session_setup.penalties.name, "FULL")
        self.assertEqual(session_setup.allowed_views.name, "Any")
        self.assertEqual(session_setup.track.name, "Zolder")
        self.assertEqual(session_setup.vehicle_class.name, "GT3")
        self.assertEqual(session_setup.date_progression, 5)
        self.assertEqual(session_setup.weather_slots, 1)
        self.assertEqual(session_setup.weather_1.name, "Clear")

        session = Session.objects.all()[0]
        session_snapshot = Session.objects.exclude(parent=None)[0]
        self.assertEqual(session.server, server_in_db)
        self.assertEqual(session.setup_actual, session_setup)
        self.assertEqual(session.planned, False)
        self.assertEqual(session.running, True)
        self.assertEqual(session.finished, False)
        self.assertEqual(session.lobby_id, '109775242847201392')
        self.assertEqual(session.max_member_count, 22)
        self.assertEqual(session.first_snapshot, session_snapshot)
        self.assertEqual(session.current_snapshot, session_snapshot)
        self.assertEqual(session.starting_snapshot_lobby, None)
        self.assertEqual(session.starting_snapshot_to_track, None)

        self.assertEqual(session_snapshot.session, session)
        self.assertEqual(session_snapshot.session_state.name, "Race")
        self.assertEqual(session_snapshot.session_stage.name, "Qualifying")
        self.assertEqual(session_snapshot.session_phase.name, "Green")
        self.assertEqual(session_snapshot.session_time_elapsed, 185)
        self.assertEqual(session_snapshot.session_time_duration, 600)
        self.assertEqual(session_snapshot.num_participants_valid, 16)
        self.assertEqual(session_snapshot.num_participants_disq, 0)
        self.assertEqual(session_snapshot.num_participants_retired, 0)
        self.assertEqual(session_snapshot.num_participants_dnf, 0)
        self.assertEqual(session_snapshot.num_participants_finished, 0)
        self.assertEqual(session_snapshot.current_year, 2015)
        self.assertEqual(session_snapshot.current_month, 7)
        self.assertEqual(session_snapshot.current_day, 6)
        self.assertEqual(session_snapshot.current_hour, 13)
        self.assertEqual(session_snapshot.current_minute, 14)
        self.assertEqual(session_snapshot.rain_density_visual, 0)
        self.assertEqual(session_snapshot.wetness_path, 0)
        self.assertEqual(session_snapshot.wetness_off_path, 0)
        self.assertEqual(session_snapshot.wetness_avg, 0)
        self.assertEqual(session_snapshot.wetness_predicted_max, 0)
        self.assertEqual(session_snapshot.wetness_max_level, 0)
        self.assertEqual(session_snapshot.temperature_ambient, 27890)
        self.assertEqual(session_snapshot.temperature_track, 39835)
        self.assertEqual(session_snapshot.air_pressure, 100760)

        member = Member.objects.all()[0]
        self.assertEqual(member.session, session)
        self.assertEqual(member.still_connected, True)
        self.assertEqual(member.vehicle.name, "McLaren 12C GT3")
        self.assertEqual(member.livery.name, "McLaren #59")
        self.assertEqual(member.refid, 26752)
        self.assertEqual(member.steam_id, '76561197969382874')
        self.assertEqual(member.name, 'blak')
        self.assertEqual(member.setup_used, True)
        self.assertEqual(member.controller_gamepad, False)
        self.assertEqual(member.controller_wheel, True)
        self.assertEqual(member.aid_steering, False)
        self.assertEqual(member.aid_braking, False)
        self.assertEqual(member.aid_abs, True)
        self.assertEqual(member.aid_traction, True)
        self.assertEqual(member.aid_stability, True)
        self.assertEqual(member.aid_no_damage, False)
        self.assertEqual(member.aid_auto_gears, False)
        self.assertEqual(member.aid_auto_clutch, True)
        self.assertEqual(member.model_normal, False)
        self.assertEqual(member.model_experienced, True)
        self.assertEqual(member.model_pro, True)
        self.assertEqual(member.model_elite, False)
        self.assertEqual(member.aid_driving_line, False)
        self.assertEqual(member.valid, True)

        m_snap = Member.objects.exclude(parent=None)[0]
        self.assertEqual(m_snap.member, member)
        self.assertEqual(m_snap.snapshot, session_snapshot)
        self.assertEqual(m_snap.still_connected, True)
        self.assertEqual(m_snap.load_state.name, MemberLoadState.admin_started_race.value)
        self.assertEqual(m_snap.ping, 14)
        self.assertEqual(m_snap.index, 0)
        self.assertEqual(m_snap.state.name, MemberState.connected.value)
        self.assertEqual(m_snap.host, True)


        member = Member.objects.all()[1]
        self.assertEqual(member.session, session)
        self.assertEqual(member.still_connected, True)
        self.assertEqual(member.vehicle.name, "Aston Martin V12 Vantage GT3")
        self.assertEqual(member.livery.name, "RaceOn OZ #55")
        self.assertEqual(member.refid, 193)
        self.assertEqual(member.steam_id, '76561198096164868')
        self.assertEqual(member.name, 'cristov822')
        self.assertEqual(member.setup_used, False)
        self.assertEqual(member.controller_gamepad, True)
        self.assertEqual(member.controller_wheel, False)
        self.assertEqual(member.aid_steering, False)
        self.assertEqual(member.aid_braking, False)
        self.assertEqual(member.aid_abs, True)
        self.assertEqual(member.aid_traction, True)
        self.assertEqual(member.aid_stability, True)
        self.assertEqual(member.aid_no_damage, False)
        self.assertEqual(member.aid_auto_gears, True)
        self.assertEqual(member.aid_auto_clutch, True)
        self.assertEqual(member.model_normal, False)
        self.assertEqual(member.model_experienced, False)
        self.assertEqual(member.model_pro, False)
        self.assertEqual(member.model_elite, True)
        self.assertEqual(member.aid_driving_line, True)
        self.assertEqual(member.valid, True)

        m_snap = Member.objects.exclude(parent=None)[1]
        self.assertEqual(m_snap.member, member)
        self.assertEqual(m_snap.snapshot, session_snapshot)
        self.assertEqual(m_snap.still_connected, True)
        self.assertEqual(m_snap.load_state.name, MemberLoadState.client_ready.value)
        self.assertEqual(m_snap.ping, 73)
        self.assertEqual(m_snap.index, 1)
        self.assertEqual(m_snap.state.name, MemberState.connected.value)
        self.assertEqual(m_snap.host, False)

        participant = Participant.objects.get(name="blak")
        self.assertEqual(participant.member, Member.objects.all()[0])
        self.assertEqual(participant.session, session)
        self.assertEqual(participant.still_connected, True)
        self.assertEqual(participant.ingame_id, 0)
        self.assertEqual(participant.refid, 26752)
        self.assertEqual(participant.name, "blak")
        self.assertEqual(participant.is_ai, False)
        self.assertEqual(participant.vehicle.name, "McLaren 12C GT3")
        self.assertEqual(participant.livery.name, "McLaren #59")

        p_snapshot = Participant.objects.exclude(parent=None).get(participant__name="blak")
        self.assertEqual(p_snapshot.snapshot, session_snapshot)
        self.assertEqual(p_snapshot.participant, participant)
        self.assertEqual(p_snapshot.still_connected, True)
        self.assertEqual(p_snapshot.grid_position, 1)
        self.assertEqual(p_snapshot.race_position, 16)
        self.assertEqual(p_snapshot.current_lap, 0)
        self.assertEqual(p_snapshot.current_sector, 0)
        self.assertEqual(p_snapshot.sector1_time, 0)
        self.assertEqual(p_snapshot.sector2_time, 0)
        self.assertEqual(p_snapshot.sector3_time, 0)
        self.assertEqual(p_snapshot.last_lap_time, 0)
        self.assertEqual(p_snapshot.fastest_lap_time, 0)
        self.assertEqual(p_snapshot.state.name, ParticipantState.in_garage.value)
        self.assertEqual(p_snapshot.headlights, False)
        self.assertEqual(p_snapshot.wipers, False)
        self.assertEqual(p_snapshot.speed, 0)
        self.assertEqual(p_snapshot.gear, 0)
        self.assertEqual(p_snapshot.rpm, 0)
        self.assertEqual(p_snapshot.position_x, 414900)
        self.assertEqual(p_snapshot.position_y, 9470)
        self.assertEqual(p_snapshot.position_z, 166000)
        self.assertEqual(p_snapshot.orientation, 182)

        participant = Participant.objects.get(name="Carlos Eduardo de Araujo")
        self.assertEqual(participant.member, None)
        self.assertEqual(participant.session, session)
        self.assertEqual(participant.still_connected, True)
        self.assertEqual(participant.ingame_id, 2)
        self.assertEqual(participant.refid, 26752)
        self.assertEqual(participant.name, "Carlos Eduardo de Araujo")
        self.assertEqual(participant.is_ai, True)
        self.assertEqual(participant.vehicle.name, "Audi R8 LMS Ultra")
        self.assertEqual(participant.livery.name, "Pedace #17")

        p_snapshot = Participant.objects.exclude(parent=None).get(participant__name="Carlos Eduardo de Araujo")
        self.assertEqual(p_snapshot.snapshot, session_snapshot)
        self.assertEqual(p_snapshot.participant, participant)
        self.assertEqual(p_snapshot.still_connected, True)
        self.assertEqual(p_snapshot.grid_position, 2)
        self.assertEqual(p_snapshot.race_position, 14)
        self.assertEqual(p_snapshot.current_lap, 1)
        self.assertEqual(p_snapshot.current_sector, 1)
        self.assertEqual(p_snapshot.sector1_time, 33832)
        self.assertEqual(p_snapshot.sector2_time, 28404)
        self.assertEqual(p_snapshot.sector3_time, 0)
        self.assertEqual(p_snapshot.last_lap_time, 0)
        self.assertEqual(p_snapshot.fastest_lap_time, 0)
        self.assertEqual(p_snapshot.state.name, ParticipantState.racing.value)
        self.assertEqual(p_snapshot.headlights, False)
        self.assertEqual(p_snapshot.wipers, False)
        self.assertEqual(p_snapshot.speed, 185)
        self.assertEqual(p_snapshot.gear, 4)
        self.assertEqual(p_snapshot.rpm, 7616)
        self.assertEqual(p_snapshot.position_x, -371490)
        self.assertEqual(p_snapshot.position_y, 6690)
        self.assertEqual(p_snapshot.position_z, -239430)
        self.assertEqual(p_snapshot.orientation, 166)

