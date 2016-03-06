import json
from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.api import ApiCaller
from autostew_back.tests.mocks import MockedRequestsResult, api_result_ok, MockedServer


class TestApi(TestCase):
    def test_send_chat(self):
        with mock.patch.object(requests, 'get', return_value=MockedRequestsResult(api_result_ok, True)):
            api = ApiCaller(MockedServer(), False, False)
            api.send_chat('Hi')

    def test_connection_fail(self):  # This test should probably be removed (tests negative case)
        with mock.patch.object(requests, 'get', side_effect=requests.exceptions.ConnectionError()):
            with self.assertRaises(requests.exceptions.ConnectionError):
                api = ApiCaller(MockedServer(), False, False)
                api.send_chat('Hi')

    # This test is either ridiculously expensive or buggy
    def disabled_test_get_lists(self):
        with open('autostew_back/tests/test_assets/lists.json') as lists_json:
            lists_result = lists_json.read()
            with mock.patch.object(
                                   requests,
                                   'get',
                                   return_value=MockedRequestsResult(lists_result, api_result_ok)
            ):
                api = ApiCaller(MockedServer(), False, False)
                self.assertDictEqual(json.loads(lists_result), api.get_lists())
