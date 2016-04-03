import os
from unittest import mock

import requests
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from autostew_back.gameserver.mocked_api import ApiReplay
from autostew_back.gameserver.server import Server as DServer
from autostew_back.plugins import db_session_writer, db_enum_writer, db, db_setup_rotation, clock, laptimes, crash_monitor, chat_notifications
from autostew_back.plugins.db_session_writer_libs import db_elo_rating, db_safety_rating
from autostew_back.tests.test_assets.settings_no_plugins import SettingsWithoutPlugins
from autostew_back.tests.unit.test_plugin_db_writer import TestDBWriter
from autostew_web_session.models import Session, RaceLapSnapshot, Server
from autostew_web_users.models import SteamUser, SafetyClass


class TestGameReplay(TestCase):
    def test_game_replay(self):
        api = ApiReplay(os.path.join(os.getcwd(), 'autostew_back', 'tests', 'test_assets', 'api_replay_hockenheim_vs_ai'))

        settings = SettingsWithoutPlugins()
        settings.plugins = [db_enum_writer]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = DServer(settings, True)
        test_setup = TestDBWriter.make_test_setup()
        test_setup.save(True)

        settings.plugins = [
            db,
            db_enum_writer,
            db_setup_rotation,
            db_session_writer,
            clock,
            laptimes,
            crash_monitor,
            chat_notifications,
        ]

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
            raise_to_this_class_threshold=db_safety_rating.initial_safety_rating - 500,
            drop_from_this_class_threshold=db_safety_rating.initial_safety_rating,
            kick_on_impact_threshold=0,
        )

        with mock.patch.object(requests, 'get', api.fake_request):
            server = DServer(settings)
            try:
                while True:
                    server.poll_loop(only_one_run=True)
                    if len(Session.objects.all()):
                        response = self.client.get(Session.objects.all().order_by('-id')[0].get_absolute_url())
                        self.assertEqual(response.status_code, 200)
            except api.RecordFinished:
                pass
        server.destroy()

        self.assertFalse(Server.objects.filter(running=True).exists())
        self.assertFalse(Session.objects.filter(running=True).exists())
        self.assertEqual(RaceLapSnapshot.objects.count(), 15)  # 15 laps
        self.assertEqual(SteamUser.objects.get(display_name="blak").elo_rating, db_elo_rating.initial_rating)
        client = Client()
        response = client.get(reverse('session:sessions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_setup.name)
        for session in Session.objects.all():
            self.assertContains(response, session.get_absolute_url())