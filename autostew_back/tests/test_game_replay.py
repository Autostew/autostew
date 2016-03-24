import os
from unittest import mock

import requests
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from autostew_back.gameserver.mocked_api import ApiReplay
from autostew_back.gameserver.server import Server as DServer
from autostew_back.plugins import db_session_writer, db_enum_writer, db, db_setup_rotation, clock, laptimes, crash_monitor, motd
from autostew_back.tests.test_assets.settings_no_plugins import SettingsWithoutPlugins
from autostew_back.tests.test_plugin_db_writer import TestDBWriter
from autostew_web_session.models import Session, RaceLapSnapshot


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
            motd,
        ]

        with mock.patch.object(requests, 'get', api.fake_request):
            server = DServer(settings)
            try:
                server.poll_loop()
            except api.RecordFinished:
                pass
        # TODO add more tests here!
        #self.assertEqual(Session.objects.count(), 2)
        #self.assertFalse(Session.objects.filter(running=True).exists())
        #self.assertEqual(RaceLapSnapshot.objects.count(), 15)
        client = Client()
        response = client.get(reverse('session:sessions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_setup.name)
        for session in Session.objects.all():
            self.assertContains(response, session.get_absolute_url())