import os
from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.mocked_api import ApiReplay
from autostew_back.gameserver.server import Server as DServer
from autostew_back.plugins import db_writer, db_enum_writer, db, db_reader, clock, laptimes, crash_monitor, motd
from autostew_back.tests.test_assets.settings_no_plugins import SettingsWithoutPlugins
from autostew_web_session.models import Session, RaceLapSnapshot


class TestGameReplay(TestCase):
    def test_game_replay(self):
        api = ApiReplay(os.path.join(os.getcwd(), 'autostew_back', 'tests', 'test_assets', 'api_replay_hockenheim_vs_ai'))
        settings = SettingsWithoutPlugins()
        settings.plugins = [
            db,
            db_reader,
            db_enum_writer,
            db_writer,
            clock,
            laptimes,
            crash_monitor,
            motd,
        ]

        with mock.patch.object(requests, 'get', api.fake_request):
            server = DServer(settings, True)
            try:
                server.poll_loop()
            except api.RecordFinished:
                pass
        # TODO add more tests here!
        self.assertEqual(Session.objects.count(), 2)
        #self.assertEqual(RaceLapSnapshot.objects.count(), 15)
