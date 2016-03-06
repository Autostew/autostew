import json
from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.api import ApiCaller
from autostew_back.tests.mocks import MockedServer, FakeApi


class TestApi(TestCase):
    def test_send_chat(self):
        api = FakeApi()
        with mock.patch.object(requests, 'get', api.fake_request):
            api = ApiCaller(MockedServer(), False, False)
            api.send_chat('Hi')

    def test_connection_fail(self):  # This test should probably be removed (tests negative case)
        with mock.patch.object(requests, 'get', side_effect=requests.exceptions.ConnectionError()):
            with self.assertRaises(requests.exceptions.ConnectionError):
                api = ApiCaller(MockedServer(), False, False)
                api.send_chat('Hi')
