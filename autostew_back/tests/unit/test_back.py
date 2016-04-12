from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.mocked_api import FakeApi
from autostew_web_enums.models import DamageDefinition, TireWearDefinition, FuelUsageDefinition, PenaltyDefinition, \
    AllowedViewsDefinition, WeatherDefinition, GameModeDefinition, PrivacyDefinition
from autostew_web_session.models.models import VehicleClass, Track, Vehicle, SetupQueueEntry
from autostew_web_session.models.server import Server, NoSessionSetupTemplateAvailableException
from autostew_back.settings import base
from autostew_web_session.models.session import SessionSetup


class TestBack(TestCase):
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
            privacy=PrivacyDefinition.objects.get_or_create(name="Public", ingame_id=2)[0],
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
    def setUp(self):
        self.server = Server.objects.create(
            name="Test",
            api_url="http://localhost:9000",
            setup_rotation_index=0,
            running=False,
        )
        self.api = FakeApi()

    def test_back_start(self):
        with mock.patch.object(requests, 'get', self.api.fake_request):
            self.server.back_start(base, False)

    def test_back_server_data(self):
        with mock.patch.object(requests, 'get', self.api.fake_request):
            self.server.back_start(base, False)
            self.assertEqual(self.server.lobby_id, 0)
            self.assertEqual(self.server.joinable_internal, False)
            self.assertEqual(self.server.max_member_count, 0)
            self.assertEqual(self.server.running, True)

    def test_back_start_running_server_without_setup(self):
        self.api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
        with mock.patch.object(requests, 'get', self.api.fake_request):
            self.assertRaises(NoSessionSetupTemplateAvailableException, self.server.back_start, base, False)

    def test_back_start_running_server_with_setup(self):
        self.api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
        setup = self.make_test_setup()
        setup.save()
        SetupQueueEntry.objects.create(order=0, setup=setup, server=self.server)
        with mock.patch.object(requests, 'get', self.api.fake_request):
            self.assertRaises(NoSessionSetupTemplateAvailableException, self.server.back_start, base, False)
