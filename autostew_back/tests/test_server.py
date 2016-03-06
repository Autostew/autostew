from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.server import Server
from autostew_back.gameserver.session import SessionFlags, Privacy, SessionState, SessionStage, SessionPhase
from autostew_back.tests.mocks import FakeApi
from autostew_back.tests.test_assets.settings_no_plugins import Settings
from autostew_back.tests.test_assets import prl_s4_r2_zolder_casual, no_setup


class TestServer(TestCase):
    def test_empty_server_construction(self):
            """
            Tests starting on an empty DS
            """
            api = FakeApi()
            with mock.patch.object(requests, 'get', api.fake_request):
                server = Server(Settings(), False)
                self.assertEqual(server.state, "Idle")
                self.assertEqual(server.lobby_id, 0)
                self.assertEqual(server.joinable, False)
                self.assertEqual(server.max_member_count, 0)

                self.assertEqual(server.get_current_setup_name(), prl_s4_r2_zolder_casual.name)
                self.assertEqual(server._setup_index, 0)
                self.assertEqual(server.session.server_controls_setup.get(), True)
                self.assertEqual(server.session.server_controls_vehicle.get(), False)
                self.assertEqual(server.session.vehicle_class.get_nice(), "GT3")
                self.assertEqual(server.session.vehicle_class.get(), -112887377)
                self.assertEqual(server.session.track.get_nice(), "Zolder")
                self.assertEqual(server.session.track.get(), -360711057)
                self.assertEqual(server.session.weather_slots.get(), 1)
                self.assertEqual(server.session.weather_1.get_nice(), "Clear")

                flags = server.session.flags.get_flags()
                self.assertNotIn(SessionFlags.abs_allowed, flags)
                self.assertNotIn(SessionFlags.force_identical_vehicles, flags)
                self.assertNotIn(SessionFlags.force_manual, flags)
                self.assertNotIn(SessionFlags.mechanical_failures, flags)
                self.assertNotIn(SessionFlags.rolling_starts, flags)
                self.assertNotIn(SessionFlags.sc_allowed, flags)
                self.assertNotIn(SessionFlags.tcs_allowed, flags)
                self.assertNotIn(SessionFlags.timed_race, flags)
                self.assertIn(SessionFlags.allow_custom_vehicle_setup, flags)
                self.assertIn(SessionFlags.auto_start_engine, flags)
                self.assertIn(SessionFlags.enforced_pitstop, flags)
                self.assertIn(SessionFlags.fill_session_with_ai, flags)
                self.assertIn(SessionFlags.force_realistic_driving_aids, flags)
                self.assertIn(SessionFlags.force_same_vehicle_class, flags)
                self.assertIn(SessionFlags.ghost_griefers, flags)

                self.assertEquals(len(server.members.elements), 0)
                self.assertEquals(len(server.participants.elements), 0)
                self.assertEquals(server.session.number_of_ai_players(), 14)

    def test_in_lobby_one_player_construction_without_setup(self):
            """
            Tests starting on an in-lobby server. No race setup is made to test if the data from the API is read
            properly (loading a setup would overwrite that data).
            """
            api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
            settings = Settings()
            settings.setup_rotation = [no_setup]
            with mock.patch.object(requests, 'get', api.fake_request):
                server = Server(settings, False)
                self.assertEqual(server.state, "Running")
                self.assertEqual(server.lobby_id, '109775242847201392')
                self.assertEqual(server.joinable, True)
                self.assertEqual(server.max_member_count, 22)

                self.assertEqual(server.get_current_setup_name(), no_setup.name)
                self.assertEqual(server._setup_index, 0)
                self.assertEqual(server.session.server_controls_setup.get(), True)
                self.assertEqual(server.session.server_controls_vehicle.get(), False)
                self.assertEqual(server.session.vehicle_class.get_nice(), "GT3")
                self.assertEqual(server.session.vehicle_class.get(), -112887377)
                self.assertEqual(server.session.track.get_nice(), "Zolder")
                self.assertEqual(server.session.track.get(), -360711057)
                self.assertEqual(server.session.weather_slots.get(), 1)
                self.assertEqual(server.session.weather_1.get_nice(), "Clear")

                flags = server.session.flags.get_flags()
                self.assertNotIn(SessionFlags.abs_allowed, flags)
                self.assertNotIn(SessionFlags.force_identical_vehicles, flags)
                self.assertNotIn(SessionFlags.force_manual, flags)
                self.assertNotIn(SessionFlags.mechanical_failures, flags)
                self.assertNotIn(SessionFlags.rolling_starts, flags)
                self.assertNotIn(SessionFlags.sc_allowed, flags)
                self.assertNotIn(SessionFlags.tcs_allowed, flags)
                self.assertNotIn(SessionFlags.timed_race, flags)
                self.assertIn(SessionFlags.allow_custom_vehicle_setup, flags)
                self.assertIn(SessionFlags.auto_start_engine, flags)
                self.assertIn(SessionFlags.enforced_pitstop, flags)
                self.assertIn(SessionFlags.fill_session_with_ai, flags)
                self.assertIn(SessionFlags.force_realistic_driving_aids, flags)
                self.assertIn(SessionFlags.force_same_vehicle_class, flags)
                self.assertIn(SessionFlags.ghost_griefers, flags)

                self.assertEquals(len(server.members.elements), 1)
                self.assertEquals(len(server.participants.elements), 0)
                self.assertEquals(server.session.number_of_ai_players(), 14)

                self.assertEqual(server.session.opponent_difficulty.get(), 100)
                self.assertEqual(server.session.practice1_length.get(), 0)
                self.assertEqual(server.session.practice2_length.get(), 0)
                self.assertEqual(server.session.qualify_length.get(), 10)
                self.assertEqual(server.session.warmup_length.get(), 0)
                self.assertEqual(server.session.race1_length.get(), 5)
                self.assertEqual(server.session.race2_length.get(), 0)
                self.assertEqual(server.session.privacy.get(), Privacy.public.value)
                self.assertEqual(server.session.privacy.get_nice(), Privacy.public)
                self.assertEqual(server.session.damage.get_nice(), "FULL")
                self.assertEqual(server.session.tire_wear.get_nice(), "X2")
                self.assertEqual(server.session.fuel_usage.get_nice(), "STANDARD")
                self.assertEqual(server.session.penalties.get_nice(), "FULL")
                self.assertEqual(server.session.allowed_views.get_nice(), "Any")
                self.assertEqual(server.session.date_year.get(), 2015)
                self.assertEqual(server.session.date_month.get(), 7)
                self.assertEqual(server.session.date_day.get(), 6)
                self.assertEqual(server.session.date_hour.get(), 13)
                self.assertEqual(server.session.date_minute.get(), 0)
                self.assertEqual(server.session.date_progression.get(), 5)
                self.assertEqual(server.session.weather_progression.get(), 1)
                self.assertEqual(server.session.track_latitude.get(), 50990)
                self.assertEqual(server.session.track_longitude.get(), 5258)
                self.assertEqual(server.session.track_altitude.get(), 37594)
                self.assertEqual(server.session.session_state.get_nice(), SessionState.lobby)
                self.assertEqual(server.session.session_stage.get_nice(), SessionStage.practice1)
                self.assertEqual(server.session.session_phase.get_nice(), SessionPhase.invalid)
                self.assertEqual(server.session.session_time_elapsed.get(), 0)
                self.assertEqual(server.session.session_time_duration.get(), 0)
                self.assertEqual(server.session.num_participants_valid.get(), 0)
                self.assertEqual(server.session.num_participants_disq.get(), 0)
                self.assertEqual(server.session.num_participants_retired.get(), 0)
                self.assertEqual(server.session.num_participants_dnf.get(), 0)
                self.assertEqual(server.session.num_participants_finished.get(), 0)
                self.assertEqual(server.session.current_year.get(), 2012)
                self.assertEqual(server.session.current_month.get(), 9)
                self.assertEqual(server.session.current_day.get(), 22)
                self.assertEqual(server.session.current_hour.get(), 6)
                self.assertEqual(server.session.current_minute.get(), 56)
                self.assertEqual(server.session.rain_density_visual.get(), 0)
                self.assertEqual(server.session.wetness_off_path.get(), 725)
                self.assertEqual(server.session.wetness_path.get(), 725)
                self.assertEqual(server.session.wetness_avg.get(), 725)
                self.assertEqual(server.session.wetness_predicted_max.get(), 0)
                self.assertEqual(server.session.wetness_max_level.get(), 725)
                self.assertEqual(server.session.temperature_ambient.get(), 21128)
                self.assertEqual(server.session.temperature_track.get(), 29692)
                self.assertEqual(server.session.air_pressure.get(), 101325)

                member = server.members.elements[0]
                self.assertEqual(member.index.get(), 0)
                self.assertEqual(member.refid.get(), 26752)
                self.assertEqual(member.steam_id.get(), '76561197969382874')
                self.assertEqual(member.state.get(), 'Connected')
                self.assertEqual(member.name.get(), 'blak')
                self.assertEqual(member.join_time.get(), 1457267561)
                self.assertEqual(member.host.get(), True)
                self.assertEqual(member.vehicle.get_nice(), "McLaren 12C GT3")
                self.assertEqual(member.vehicle.get(), -1166911988)
                self.assertEqual(member.load_state.get(), "UNKNOWN")
                self.assertEqual(len(member.race_stat_flags.get_flags()), 0)
                self.assertEqual(member.ping.get(), 10)
                # self.assertEqual(member.livery.get_nice(), "McLaren #59") TODO but not so important
                self.assertEqual(member.livery.get(), 51)
