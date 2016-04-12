from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.mocked_api import FakeApi
from autostew_web_session.models.server import Server
from autostew_back.settings import base


class TestBack(TestCase):
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

    def test_back_start_running_server(self):
        self.api = FakeApi('autostew_back/tests/test_assets/session_in_lobby_one_player.json')
        with mock.patch.object(requests, 'get', self.api.fake_request):
            self.server.back_start(base, False)
            self.assertEqual(self.server.lobby_id, 0)
            self.assertEqual(self.server.joinable_internal, False)
            self.assertEqual(self.server.max_member_count, 0)
            self.assertEqual(self.server.running, True)

