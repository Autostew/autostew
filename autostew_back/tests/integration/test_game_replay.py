import os
from unittest import mock

import requests
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from autostew_back import settings
from autostew_back.ds_api.mocked_api import ApiReplay, FakeApi
from autostew_back.tests.unit.test_back import TestBack
from autostew_web_session.models.models import RaceLapSnapshot, SetupRotationEntry
from autostew_web_session.models.server import Server
from autostew_web_session.models.session import Session
from autostew_web_users.models import SteamUser, SafetyClass


class TestGameReplay(TestCase):
    def setUp(self):
        self.server = Server.objects.create(
            name="Test",
            api_url="http://localhost:9000",
            setup_rotation_index=0,
            running=False,
        )
        self.api = FakeApi()

    def test_game_replay(self):
        api = ApiReplay(os.path.join(os.getcwd(), 'autostew_back', 'tests', 'test_assets', 'api_replay_hockenheim_vs_ai'))

        with mock.patch.object(requests, 'get', api.fake_request):
            self.server.back_start(settings, True)
        test_setup = TestBack.make_test_setup()
        test_setup.save(True)
        SetupRotationEntry.objects.create(
            order=0,
            server=self.server,
            setup=test_setup
        )

        b = SafetyClass.objects.create(
            order=1,
            name='B',
            raise_to_this_class_threshold=0,
            drop_from_this_class_threshold=0,
            kick_on_impact_threshold=900,
            initial_class=True,
        )

        SafetyClass.objects.create(
            order=0,
            name='A',
            class_below=b,
            raise_to_this_class_threshold=SteamUser.initial_safety_rating - 500,
            drop_from_this_class_threshold=SteamUser.initial_safety_rating,
            kick_on_impact_threshold=0,
        )

        settings.event_poll_period = 0
        settings.full_update_period = 0

        with mock.patch.object(requests, 'get', api.fake_request):
            self.server.back_start(settings, False)
            try:
                while True:
                    self.server.back_poll_loop(only_one_run=True)
                    # TODO comment this back in
                    if len(Session.objects.all()):
                        response = self.client.get(Session.objects.all().order_by('-id')[0].get_absolute_url())
                        self.assertEqual(response.status_code, 200)
            except api.RecordFinished:
                pass
        self.server.back_destroy()

        self.assertFalse(Server.objects.filter(running=True).exists())
        self.assertEqual(RaceLapSnapshot.objects.count(), 15)  # 15 laps
        self.assertEqual(SteamUser.objects.get(display_name="blak").elo_rating, SteamUser.initial_elo_rating)
        client = Client()
        response = client.get(reverse('session:sessions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_setup.name)
        for session in Session.objects.all():
            if session.finished and session.parent is None:
                self.assertContains(response, session.get_absolute_url())
            else:
                pass
                # TODO self.assertNotContains(response, session.get_absolute_url())
