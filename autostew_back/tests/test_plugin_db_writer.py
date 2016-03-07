import json
from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.member import MemberLoadState, MemberState
from autostew_back.gameserver.server import Server as DServer, UnmetPluginDependency
from autostew_back.plugins import db_enum_writer, db, db_writer
from autostew_back.tests.mocks import FakeApi
from autostew_back.tests.test_assets.settings_no_plugins import SettingsWithoutPlugins
from autostew_web_session.models import Session, SessionSetup, Participant, SessionSnapshot, Member, MemberSnapshot, \
    ParticipantSnapshot
from autostew_web_session import models


class TestDBWriter(TestCase):
    def test_dependency(self):
        api = FakeApi()
        settings = SettingsWithoutPlugins()
        with mock.patch.object(requests, 'get', api.fake_request):
            settings.plugins = [db_writer]
            self.assertRaises(UnmetPluginDependency, DServer, settings, False)
        with mock.patch.object(requests, 'get', api.fake_request):
            settings.plugins = [db, db_writer]
            self.assertRaises(UnmetPluginDependency, DServer, settings, False)
        with mock.patch.object(requests, 'get', api.fake_request):
            settings.plugins = [db_enum_writer, db_writer]
            self.assertRaises(UnmetPluginDependency, DServer, settings, False)

    def test_create_session(self):
        api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
        settings = SettingsWithoutPlugins()
        settings.plugins = [db, db_enum_writer, db_writer]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = DServer(settings, True)
        self.assertEqual(models.Server.objects.count(), 1)
        self.assertEqual(SessionSetup.objects.count(), 1)
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(SessionSnapshot.objects.count(), 1)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(MemberSnapshot.objects.count(), 1)
        self.assertEqual(Participant.objects.count(), 0)
        self.assertEqual(ParticipantSnapshot.objects.count(), 0)

        server_in_db = models.Server.objects.all()[0]
        self.assertEqual(server_in_db.name, settings.server_name)
        self.assertTrue(server_in_db.running)

        session_setup = models.SessionSetup.objects.all()[0]
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
        session_snapshot = SessionSnapshot.objects.all()[0]
        self.assertEqual(session.server, server_in_db)
        self.assertEqual(session.setup, session_setup)
        self.assertEqual(session.planned, False)
        self.assertEqual(session.running, True)
        self.assertEqual(session.finished, False)
        self.assertEqual(session.lobby_id, '109775242847201392')
        self.assertEqual(session.max_member_count, 22)
        self.assertEqual(session.first_snapshot, session_snapshot)
        self.assertEqual(session.current_snapshot, session_snapshot)
        self.assertEqual(session.starting_snapshot_lobby, None)
        self.assertEqual(session.starting_snapshot_to_track, None)
        self.assertEqual(session.starting_snapshot_practice1, None)
        self.assertEqual(session.starting_snapshot_practice2, None)
        self.assertEqual(session.starting_snapshot_qualifying, None)
        self.assertEqual(session.starting_snapshot_warmup, None)
        self.assertEqual(session.starting_snapshot_race, None)
        self.assertEqual(session.ending_snapshot_race, None)

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

        m_snap = MemberSnapshot.objects.all()[0]
        self.assertEqual(m_snap.member, member)
        self.assertEqual(m_snap.snapshot, session_snapshot)
        self.assertEqual(m_snap.still_connected, True)
        self.assertEqual(m_snap.load_state.name, MemberLoadState.unknown.value)
        self.assertEqual(m_snap.ping, 10)
        self.assertEqual(m_snap.index, 0)
        self.assertEqual(m_snap.state.name, MemberState.connected.value)
        self.assertEqual(m_snap.host, True)
