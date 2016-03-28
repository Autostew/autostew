from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.member import MemberLoadState, MemberFlags, MemberState
from autostew_back.gameserver.mocked_api import FakeApi
from autostew_back.gameserver.participant import ParticipantState
from autostew_back.gameserver.server import Server, ServerState
from autostew_back.gameserver.session import SessionFlags, Privacy, SessionState, SessionStage, SessionPhase
from autostew_back.plugins import local_setup_rotation
from autostew_back.tests.test_assets import prl_s4_r2_zolder_casual, no_setup
from autostew_back.tests.test_assets.settings_no_plugins import SettingsWithoutPlugins


def status_empty(test_case, server):
    """
    Test for status after appliying prl_s4_r2_zolder_casual setup to an empty lobby
    """
    test_case.assertEqual(server.state, ServerState.idle)
    test_case.assertEqual(server.lobby_id, 0)
    test_case.assertEqual(server.joinable, False)
    test_case.assertEqual(server.max_member_count, 0)

    test_case.assertEqual(server.get_current_setup_name(), prl_s4_r2_zolder_casual.name)
    test_case.assertEqual(server.session.server_controls_setup.get(), True)
    test_case.assertEqual(server.session.server_controls_vehicle.get(), False)
    test_case.assertEqual(server.session.vehicle_class.get_nice(), "GT3")
    test_case.assertEqual(server.session.vehicle_class.get(), -112887377)
    test_case.assertEqual(server.session.track.get_nice(), "Zolder")
    test_case.assertEqual(server.session.track.get(), -360711057)
    test_case.assertEqual(server.session.weather_slots.get(), 1)
    test_case.assertEqual(server.session.weather_1.get_nice(), "Clear")

    flags = server.session.flags.get_flags()
    test_case.assertNotIn(SessionFlags.abs_allowed, flags)
    test_case.assertNotIn(SessionFlags.force_identical_vehicles, flags)
    test_case.assertNotIn(SessionFlags.force_manual, flags)
    test_case.assertNotIn(SessionFlags.mechanical_failures, flags)
    test_case.assertNotIn(SessionFlags.rolling_starts, flags)
    test_case.assertNotIn(SessionFlags.sc_allowed, flags)
    test_case.assertNotIn(SessionFlags.tcs_allowed, flags)
    test_case.assertNotIn(SessionFlags.timed_race, flags)
    test_case.assertIn(SessionFlags.allow_custom_vehicle_setup, flags)
    test_case.assertIn(SessionFlags.auto_start_engine, flags)
    test_case.assertIn(SessionFlags.enforced_pitstop, flags)
    test_case.assertIn(SessionFlags.fill_session_with_ai, flags)
    test_case.assertIn(SessionFlags.force_realistic_driving_aids, flags)
    test_case.assertIn(SessionFlags.force_same_vehicle_class, flags)
    test_case.assertIn(SessionFlags.ghost_griefers, flags)

    test_case.assertEquals(len(server.members.elements), 0)
    test_case.assertEquals(len(server.participants.elements), 0)
    test_case.assertEquals(server.session.number_of_ai_players(), 14)


def status_in_lobby(test_case, server):
    """
    Test for server status after loading session_in_lobby_one_player.json
    """
    test_case.assertEqual(server.state, ServerState.running)
    test_case.assertEqual(server.lobby_id, '109775242847201392')
    test_case.assertEqual(server.joinable, True)
    test_case.assertEqual(server.max_member_count, 22)
    test_case.assertEqual(server.get_current_setup_name(), no_setup.name)
    test_case.assertEqual(server.session.server_controls_setup.get(), True)
    test_case.assertEqual(server.session.server_controls_vehicle.get(), False)
    test_case.assertEqual(server.session.vehicle_class.get_nice(), "GT3")
    test_case.assertEqual(server.session.vehicle_class.get(), -112887377)
    test_case.assertEqual(server.session.track.get_nice(), "Zolder")
    test_case.assertEqual(server.session.track.get(), -360711057)
    test_case.assertEqual(server.session.weather_slots.get(), 1)
    test_case.assertEqual(server.session.weather_1.get_nice(), "Clear")
    flags = server.session.flags.get_flags()
    test_case.assertNotIn(SessionFlags.abs_allowed, flags)
    test_case.assertNotIn(SessionFlags.force_identical_vehicles, flags)
    test_case.assertNotIn(SessionFlags.force_manual, flags)
    test_case.assertNotIn(SessionFlags.mechanical_failures, flags)
    test_case.assertNotIn(SessionFlags.rolling_starts, flags)
    test_case.assertNotIn(SessionFlags.sc_allowed, flags)
    test_case.assertNotIn(SessionFlags.tcs_allowed, flags)
    test_case.assertNotIn(SessionFlags.timed_race, flags)
    test_case.assertIn(SessionFlags.allow_custom_vehicle_setup, flags)
    test_case.assertIn(SessionFlags.auto_start_engine, flags)
    test_case.assertIn(SessionFlags.enforced_pitstop, flags)
    test_case.assertIn(SessionFlags.fill_session_with_ai, flags)
    test_case.assertIn(SessionFlags.force_realistic_driving_aids, flags)
    test_case.assertIn(SessionFlags.force_same_vehicle_class, flags)
    test_case.assertIn(SessionFlags.ghost_griefers, flags)
    test_case.assertEquals(len(server.members.elements), 1)
    test_case.assertEquals(len(server.participants.elements), 0)
    test_case.assertEquals(server.session.number_of_ai_players(), 14)
    test_case.assertEqual(server.session.opponent_difficulty.get(), 100)
    test_case.assertEqual(server.session.practice1_length.get(), 0)
    test_case.assertEqual(server.session.practice2_length.get(), 0)
    test_case.assertEqual(server.session.qualify_length.get(), 10)
    test_case.assertEqual(server.session.warmup_length.get(), 0)
    test_case.assertEqual(server.session.race1_length.get(), 5)
    test_case.assertEqual(server.session.race2_length.get(), 0)
    test_case.assertEqual(server.session.privacy.get(), Privacy.public.value)
    test_case.assertEqual(server.session.privacy.get_nice(), Privacy.public)
    test_case.assertEqual(server.session.damage.get_nice(), "FULL")
    test_case.assertEqual(server.session.tire_wear.get_nice(), "X2")
    test_case.assertEqual(server.session.fuel_usage.get_nice(), "STANDARD")
    test_case.assertEqual(server.session.penalties.get_nice(), "FULL")
    test_case.assertEqual(server.session.allowed_views.get_nice(), "Any")
    test_case.assertEqual(server.session.date_year.get(), 2015)
    test_case.assertEqual(server.session.date_month.get(), 7)
    test_case.assertEqual(server.session.date_day.get(), 6)
    test_case.assertEqual(server.session.date_hour.get(), 13)
    test_case.assertEqual(server.session.date_minute.get(), 0)
    test_case.assertEqual(server.session.date_progression.get(), 5)
    test_case.assertEqual(server.session.weather_progression.get(), 1)
    test_case.assertEqual(server.session.track_latitude.get(), 50990)
    test_case.assertEqual(server.session.track_longitude.get(), 5258)
    test_case.assertEqual(server.session.track_altitude.get(), 37594)
    test_case.assertEqual(server.session.session_state.get_nice(), SessionState.lobby)
    test_case.assertEqual(server.session.session_stage.get_nice(), SessionStage.practice1)
    test_case.assertEqual(server.session.session_phase.get_nice(), SessionPhase.invalid)
    test_case.assertEqual(server.session.session_time_elapsed.get(), 0)
    test_case.assertEqual(server.session.session_time_duration.get(), 0)
    test_case.assertEqual(server.session.num_participants_valid.get(), 0)
    test_case.assertEqual(server.session.num_participants_disq.get(), 0)
    test_case.assertEqual(server.session.num_participants_retired.get(), 0)
    test_case.assertEqual(server.session.num_participants_dnf.get(), 0)
    test_case.assertEqual(server.session.num_participants_finished.get(), 0)
    test_case.assertEqual(server.session.current_year.get(), 2012)
    test_case.assertEqual(server.session.current_month.get(), 9)
    test_case.assertEqual(server.session.current_day.get(), 22)
    test_case.assertEqual(server.session.current_hour.get(), 6)
    test_case.assertEqual(server.session.current_minute.get(), 56)
    test_case.assertEqual(server.session.rain_density_visual.get(), 0)
    test_case.assertEqual(server.session.wetness_off_path.get(), 725)
    test_case.assertEqual(server.session.wetness_path.get(), 725)
    test_case.assertEqual(server.session.wetness_avg.get(), 725)
    test_case.assertEqual(server.session.wetness_predicted_max.get(), 0)
    test_case.assertEqual(server.session.wetness_max_level.get(), 725)
    test_case.assertEqual(server.session.temperature_ambient.get(), 21128)
    test_case.assertEqual(server.session.temperature_track.get(), 29692)
    test_case.assertEqual(server.session.air_pressure.get(), 101325)


def members_one_player_lobby(test_case, server):
    """
    Checks members after loading session_in_lobby_one_player.json
    """
    member = server.members.elements[0]
    test_case.assertEqual(member.index.get(), 0)
    test_case.assertEqual(member.refid.get(), 26752)
    test_case.assertEqual(member.steam_id.get(), '76561197969382874')
    test_case.assertEqual(member.state.get(), 'Connected')
    test_case.assertEqual(member.state.get_nice(), MemberState.connected)
    test_case.assertEqual(member.name.get(), 'blak')
    test_case.assertEqual(member.join_time.get(), 1457267561)
    test_case.assertEqual(member.host.get(), True)
    test_case.assertEqual(member.vehicle.get_nice(), "McLaren 12C GT3")
    test_case.assertEqual(member.vehicle.get(), -1166911988)
    test_case.assertEqual(member.load_state.get(), "UNKNOWN")
    test_case.assertEqual(member.load_state.get_nice(), MemberLoadState.unknown)
    test_case.assertEqual(len(member.race_stat_flags.get_flags()), 0)
    test_case.assertEqual(member.ping.get(), 10)
    # test_case.assertEqual(member.livery.get_nice(), "McLaren #59") TODO but not so important
    test_case.assertEqual(member.livery.get(), 51)


def status_quali(test_case, server):
    """
    Test session after loading session_in_quali_two_players_14ai.json
    """
    test_case.assertEqual(server.state, ServerState.running)
    test_case.assertEqual(server.lobby_id, '109775242847201392')
    test_case.assertEqual(server.joinable, True)
    test_case.assertEqual(server.max_member_count, 22)

    test_case.assertEqual(server.get_current_setup_name(), no_setup.name)
    test_case.assertEqual(server.session.server_controls_setup.get(), True)
    test_case.assertEqual(server.session.server_controls_vehicle.get(), False)
    test_case.assertEqual(server.session.vehicle_class.get_nice(), "GT3")
    test_case.assertEqual(server.session.vehicle_class.get(), -112887377)
    test_case.assertEqual(server.session.track.get_nice(), "Zolder")
    test_case.assertEqual(server.session.track.get(), -360711057)
    test_case.assertEqual(server.session.weather_slots.get(), 1)
    test_case.assertEqual(server.session.weather_1.get_nice(), "Clear")

    flags = server.session.flags.get_flags()
    test_case.assertNotIn(SessionFlags.abs_allowed, flags)
    test_case.assertNotIn(SessionFlags.force_identical_vehicles, flags)
    test_case.assertNotIn(SessionFlags.force_manual, flags)
    test_case.assertNotIn(SessionFlags.mechanical_failures, flags)
    test_case.assertNotIn(SessionFlags.rolling_starts, flags)
    test_case.assertNotIn(SessionFlags.sc_allowed, flags)
    test_case.assertNotIn(SessionFlags.tcs_allowed, flags)
    test_case.assertNotIn(SessionFlags.timed_race, flags)
    test_case.assertIn(SessionFlags.allow_custom_vehicle_setup, flags)
    test_case.assertIn(SessionFlags.auto_start_engine, flags)
    test_case.assertIn(SessionFlags.enforced_pitstop, flags)
    test_case.assertIn(SessionFlags.fill_session_with_ai, flags)
    test_case.assertIn(SessionFlags.force_realistic_driving_aids, flags)
    test_case.assertIn(SessionFlags.force_same_vehicle_class, flags)
    test_case.assertIn(SessionFlags.ghost_griefers, flags)

    test_case.assertEquals(len(server.members.elements), 2)
    test_case.assertEquals(len(server.participants.elements), 16)
    test_case.assertEquals(server.session.number_of_ai_players(), 14)

    test_case.assertEqual(server.session.opponent_difficulty.get(), 100)
    test_case.assertEqual(server.session.practice1_length.get(), 0)
    test_case.assertEqual(server.session.practice2_length.get(), 0)
    test_case.assertEqual(server.session.qualify_length.get(), 10)
    test_case.assertEqual(server.session.warmup_length.get(), 0)
    test_case.assertEqual(server.session.race1_length.get(), 5)
    test_case.assertEqual(server.session.race2_length.get(), 0)
    test_case.assertEqual(server.session.privacy.get(), Privacy.public.value)
    test_case.assertEqual(server.session.privacy.get_nice(), Privacy.public)
    test_case.assertEqual(server.session.damage.get_nice(), "FULL")
    test_case.assertEqual(server.session.tire_wear.get_nice(), "X2")
    test_case.assertEqual(server.session.fuel_usage.get_nice(), "STANDARD")
    test_case.assertEqual(server.session.penalties.get_nice(), "FULL")
    test_case.assertEqual(server.session.allowed_views.get_nice(), "Any")
    test_case.assertEqual(server.session.date_year.get(), 2015)
    test_case.assertEqual(server.session.date_month.get(), 7)
    test_case.assertEqual(server.session.date_day.get(), 6)
    test_case.assertEqual(server.session.date_hour.get(), 13)
    test_case.assertEqual(server.session.date_minute.get(), 0)
    test_case.assertEqual(server.session.date_progression.get(), 5)
    test_case.assertEqual(server.session.weather_progression.get(), 1)
    test_case.assertEqual(server.session.track_latitude.get(), 50990)
    test_case.assertEqual(server.session.track_longitude.get(), 5258)
    test_case.assertEqual(server.session.track_altitude.get(), 37594)
    test_case.assertEqual(server.session.session_state.get_nice(), SessionState.race)
    test_case.assertEqual(server.session.session_stage.get_nice(), SessionStage.qualifying)
    test_case.assertEqual(server.session.session_phase.get_nice(), SessionPhase.green)
    test_case.assertEqual(server.session.session_time_elapsed.get(), 185)
    test_case.assertEqual(server.session.session_time_duration.get(), 600)
    test_case.assertEqual(server.session.num_participants_valid.get(), 16)
    test_case.assertEqual(server.session.num_participants_disq.get(), 0)
    test_case.assertEqual(server.session.num_participants_retired.get(), 0)
    test_case.assertEqual(server.session.num_participants_dnf.get(), 0)
    test_case.assertEqual(server.session.num_participants_finished.get(), 0)
    test_case.assertEqual(server.session.current_year.get(), 2015)
    test_case.assertEqual(server.session.current_month.get(), 7)
    test_case.assertEqual(server.session.current_day.get(), 6)
    test_case.assertEqual(server.session.current_hour.get(), 13)
    test_case.assertEqual(server.session.current_minute.get(), 14)
    test_case.assertEqual(server.session.rain_density_visual.get(), 0)
    test_case.assertEqual(server.session.wetness_off_path.get(), 0)
    test_case.assertEqual(server.session.wetness_path.get(), 0)
    test_case.assertEqual(server.session.wetness_avg.get(), 0)
    test_case.assertEqual(server.session.wetness_predicted_max.get(), 0)
    test_case.assertEqual(server.session.wetness_max_level.get(), 0)
    test_case.assertEqual(server.session.temperature_ambient.get(), 27890)
    test_case.assertEqual(server.session.temperature_track.get(), 39835)
    test_case.assertEqual(server.session.air_pressure.get(), 100760)

    test_case.assertEqual(server.members.elements[1], server.members.get_by_id(193))
    test_case.assertEqual(server.members.elements[1], server.members.get_by_property('steam_id', '76561198096164868'))


def members_in_quali(test_case, server):
    member = server.members.elements[0]
    test_case.assertEqual(member.index.get(), 0)
    test_case.assertEqual(member.refid.get(), 26752)
    test_case.assertEqual(member.steam_id.get(), '76561197969382874')
    test_case.assertEqual(member.state.get(), 'Connected')
    test_case.assertEqual(member.state.get_nice(), MemberState.connected)
    test_case.assertEqual(member.name.get(), 'blak')
    test_case.assertEqual(member.join_time.get(), 1457267561)
    test_case.assertEqual(member.host.get(), True)
    test_case.assertEqual(member.vehicle.get_nice(), "McLaren 12C GT3")
    test_case.assertEqual(member.vehicle.get(), -1166911988)
    test_case.assertEqual(member.load_state.get_nice(), MemberLoadState.admin_started_race)
    test_case.assertEqual(len(member.race_stat_flags.get_flags()), 11)

    flags = member.race_stat_flags.get_flags()
    test_case.assertIn(MemberFlags.setup_used, flags)
    test_case.assertNotIn(MemberFlags.controller_gamepad, flags)
    test_case.assertIn(MemberFlags.controller_wheel, flags)
    test_case.assertIn(MemberFlags.controller_mask, flags)
    test_case.assertNotIn(MemberFlags.aid_steering, flags)
    test_case.assertNotIn(MemberFlags.aid_braking, flags)
    test_case.assertIn(MemberFlags.aid_abs, flags)
    test_case.assertIn(MemberFlags.aid_traction, flags)
    test_case.assertIn(MemberFlags.aid_stability, flags)
    test_case.assertNotIn(MemberFlags.aid_no_damage, flags)
    test_case.assertNotIn(MemberFlags.aid_auto_gears, flags)
    test_case.assertIn(MemberFlags.aid_auto_clutch, flags)
    test_case.assertNotIn(MemberFlags.model_normal, flags)
    test_case.assertIn(MemberFlags.model_experienced, flags)
    test_case.assertIn(MemberFlags.model_pro, flags)
    test_case.assertNotIn(MemberFlags.model_elite, flags)
    test_case.assertIn(MemberFlags.model_mask, flags)
    test_case.assertNotIn(MemberFlags.aid_driving_line, flags)
    test_case.assertIn(MemberFlags.valid, flags)

    test_case.assertEqual(member.ping.get(), 14)
    # test_case.assertEqual(member.livery.get_nice(), "McLaren #59") TODO but not so important
    test_case.assertEqual(member.livery.get(), 51)

    member = server.members.elements[1]
    test_case.assertEqual(member.index.get(), 1)
    test_case.assertEqual(member.refid.get(), 193)
    test_case.assertEqual(member.steam_id.get(), '76561198096164868')
    test_case.assertEqual(member.state.get(), 'Connected')
    test_case.assertEqual(member.state.get_nice(), MemberState.connected)
    test_case.assertEqual(member.name.get(), 'cristov822')
    test_case.assertEqual(member.join_time.get(), 1457268515)
    test_case.assertEqual(member.host.get(), False)
    test_case.assertEqual(member.vehicle.get_nice(), "Aston Martin V12 Vantage GT3")
    test_case.assertEqual(member.load_state.get_nice(), MemberLoadState.client_ready)
    test_case.assertEqual(len(member.race_stat_flags.get_flags()), 11)

    flags = member.race_stat_flags.get_flags()
    test_case.assertNotIn(MemberFlags.setup_used, flags)
    test_case.assertIn(MemberFlags.controller_gamepad, flags)
    test_case.assertNotIn(MemberFlags.controller_wheel, flags)
    test_case.assertIn(MemberFlags.controller_mask, flags)
    test_case.assertNotIn(MemberFlags.aid_steering, flags)
    test_case.assertNotIn(MemberFlags.aid_braking, flags)
    test_case.assertIn(MemberFlags.aid_abs, flags)
    test_case.assertIn(MemberFlags.aid_traction, flags)
    test_case.assertIn(MemberFlags.aid_stability, flags)
    test_case.assertNotIn(MemberFlags.aid_no_damage, flags)
    test_case.assertIn(MemberFlags.aid_auto_gears, flags)
    test_case.assertIn(MemberFlags.aid_auto_clutch, flags)
    test_case.assertNotIn(MemberFlags.model_normal, flags)
    test_case.assertNotIn(MemberFlags.model_experienced, flags)
    test_case.assertNotIn(MemberFlags.model_pro, flags)
    test_case.assertIn(MemberFlags.model_elite, flags)
    test_case.assertIn(MemberFlags.model_mask, flags)
    test_case.assertIn(MemberFlags.aid_driving_line, flags)
    test_case.assertIn(MemberFlags.valid, flags)

    test_case.assertEqual(member.ping.get(), 73)
    # test_case.assertEqual(member.livery.get_nice(), "McLaren #59") TODO but not so important
    test_case.assertEqual(member.livery.get(), 74)


def participants_in_quali(test_case, server):
    test_case.assertEqual(server.participants.get_by_id(0), server.participants.elements[0])
    test_case.assertEqual(server.participants.get_by_id(1), server.participants.elements[1])
    test_case.assertEqual(server.participants.get_by_property('refid', 193), server.participants.elements[1])
    test_case.assertEqual(server.participants.get_by_property('name', 'blak'), server.participants.elements[0])
    test_case.assertIn(server.participants.elements[0], server.participants.get_by_property('is_player', True, unique=False))
    test_case.assertIn(server.participants.elements[1], server.participants.get_by_property('is_player', True, unique=False))
    test_case.assertNotIn(server.participants.elements[2], server.participants.get_by_property('is_player', True, unique=False))

    participant = server.participants.get_by_id(0)
    test_case.assertEqual(participant.refid.get(), 26752)
    test_case.assertEqual(participant.name.get(), 'blak')
    test_case.assertEqual(participant.is_player.get(), True)
    test_case.assertEqual(participant.grid_position.get(), 1)
    test_case.assertEqual(participant.vehicle.get_nice(), "McLaren 12C GT3")
    test_case.assertEqual(participant.livery.get(), 51)
    test_case.assertEqual(participant.race_position.get(), 16)
    test_case.assertEqual(participant.current_lap.get(), 0)
    test_case.assertEqual(participant.current_sector.get(), 0)
    test_case.assertEqual(participant.sector1_time.get(), 0)
    test_case.assertEqual(participant.sector2_time.get(), 0)
    test_case.assertEqual(participant.sector3_time.get(), 0)
    test_case.assertEqual(participant.last_lap_time.get(), 0)
    test_case.assertEqual(participant.fastest_lap_time.get(), 0)
    test_case.assertEqual(participant.state.get_nice(), ParticipantState.in_garage)
    test_case.assertEqual(participant.headlights.get(), False)
    test_case.assertEqual(participant.wipers.get(), False)
    test_case.assertEqual(participant.gear.get(), 0)
    test_case.assertEqual(participant.speed.get(), 0)
    test_case.assertEqual(participant.rpm.get(), 0)
    test_case.assertEqual(participant.position_x.get(), 414900)
    test_case.assertEqual(participant.position_y.get(), 9470)
    test_case.assertEqual(participant.position_z.get(), 166000)
    test_case.assertEqual(participant.orientation.get(), 182)

    participant = server.participants.get_by_id(2)
    test_case.assertEqual(participant.refid.get(), 26752)
    test_case.assertEqual(participant.name.get(), 'Carlos Eduardo de Araujo')
    test_case.assertEqual(participant.is_player.get(), False)
    test_case.assertEqual(participant.grid_position.get(), 2)
    test_case.assertEqual(participant.vehicle.get_nice(), "Audi R8 LMS Ultra")
    test_case.assertEqual(participant.livery.get(), 55)
    test_case.assertEqual(participant.race_position.get(), 14)
    test_case.assertEqual(participant.current_lap.get(), 1)
    test_case.assertEqual(participant.current_sector.get(), 1)
    test_case.assertEqual(participant.sector1_time.get(), 33832)
    test_case.assertEqual(participant.sector2_time.get(), 28404)
    test_case.assertEqual(participant.sector3_time.get(), 0)
    test_case.assertEqual(participant.last_lap_time.get(), 0)
    test_case.assertEqual(participant.fastest_lap_time.get(), 0)
    test_case.assertEqual(participant.state.get_nice(), ParticipantState.racing)
    test_case.assertEqual(participant.headlights.get(), False)
    test_case.assertEqual(participant.wipers.get(), False)
    test_case.assertEqual(participant.gear.get(), 4)
    test_case.assertEqual(participant.speed.get(), 185)
    test_case.assertEqual(participant.rpm.get(), 7616)
    test_case.assertEqual(participant.position_x.get(), -371490)
    test_case.assertEqual(participant.position_y.get(), 6690)
    test_case.assertEqual(participant.position_z.get(), -239430)
    test_case.assertEqual(participant.orientation.get(), 166)

class TestServer(TestCase):
    def test_empty_server_construction(self):
        """
        Tests starting autostew_back on an empty DS
        """
        api = FakeApi()
        with mock.patch.object(requests, 'get', api.fake_request):
            server = Server(SettingsWithoutPlugins(), False)
            local_setup_rotation.load_next_setup(server)
            status_empty(self, server)

    def test_in_lobby_one_player_setup_without_setup(self):
        """
        Tests starting on an in-lobby server. No race setup is made to test if the data from the API is read
        properly (loading a setup would overwrite that data).
        """
        api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
        settings = SettingsWithoutPlugins()
        settings.setup_rotation = [no_setup]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = Server(settings, False)
            local_setup_rotation.load_next_setup(server)
            status_in_lobby(self, server)

    def test_in_lobby_one_player_members_without_setup(self):
        """
        Tests starting on an in-lobby server. No race setup is made to test if the data from the API is read
        properly (loading a setup would overwrite that data).
        """
        api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
        settings = SettingsWithoutPlugins()
        settings.setup_rotation = [no_setup]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = Server(settings, False)
            local_setup_rotation.load_next_setup(server)
            members_one_player_lobby(self, server)

    def test_setup_in_quali_two_player_14_ai_setup_without_setup(self):
        """
        Tests starting on an in-qualifying server. No race setup is made to test if the data from the API is read
        properly (loading a setup would overwrite that data).
        """
        api = FakeApi('autostew_back/tests/test_assets/session_in_quali_two_players_14ai.json')
        settings = SettingsWithoutPlugins()
        settings.setup_rotation = [no_setup]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = Server(settings, False)
            local_setup_rotation.load_next_setup(server)
            status_quali(self, server)

    def test_setup_in_quali_two_player_14_ai_members_without_setup(self):
        """
        Tests starting on an in-qualifying server. No race setup is made to test if the data from the API is read
        properly (loading a setup would overwrite that data).
        """
        api = FakeApi('autostew_back/tests/test_assets/session_in_quali_two_players_14ai.json')
        settings = SettingsWithoutPlugins()
        settings.setup_rotation = [no_setup]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = Server(settings, False)
            local_setup_rotation.load_next_setup(server)
            members_in_quali(self, server)

    def test_setup_in_quali_two_player_14_ai_participants_without_setup(self):
        """
        Tests starting on an in-qualifying server. No race setup is made to test if the data from the API is read
        properly (loading a setup would overwrite that data).
        """
        api = FakeApi('autostew_back/tests/test_assets/session_in_quali_two_players_14ai.json')
        settings = SettingsWithoutPlugins()
        settings.setup_rotation = [no_setup]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = Server(settings, False)
            local_setup_rotation.load_next_setup(server)
            participants_in_quali(self, server)

    def test_status_progression(self):
        """
        Tests fetching different status several times.
        """
        api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
        settings = SettingsWithoutPlugins()
        settings.setup_rotation = [no_setup]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = Server(settings, False)
            local_setup_rotation.load_next_setup(server)
            status_in_lobby(self, server)
            api.status_result = 'autostew_back/tests/test_assets/session_in_quali_two_players_14ai.json'
            server.fetch_status()
            status_quali(self, server)
            members_in_quali(self, server)
            participants_in_quali(self, server)
            api.status_result = 'autostew_back/tests/test_assets/session_in_race_one_player_14ai.json'
            server.fetch_status()
            self.assertEqual(server.state, ServerState.running)
            self.assertEqual(server.joinable, False)
            self.assertEqual(server.session.session_state.get_nice(), SessionState.race)
            self.assertEqual(server.session.session_stage.get_nice(), SessionStage.race1)
            self.assertEqual(server.session.session_phase.get_nice(), SessionPhase.green)
            self.assertEqual(len(server.members.elements), 1)
            self.assertEqual(len(server.participants.elements), 15)
