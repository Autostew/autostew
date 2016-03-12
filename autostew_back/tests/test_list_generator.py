from unittest import mock

import requests
from django.test import TestCase

from autostew_back.gameserver.api import ApiCaller
from autostew_back.gameserver.lists import ListGenerator, ListName
from autostew_back.gameserver.mocked_api import api_result_ok, MockedRequestsResult, MockedServer


class TestLists(TestCase):
    def get_lists(self):
        with open('autostew_back/tests/test_assets/lists.json') as lists_json:
            with mock.patch.object(
                                   requests,
                                   'get',
                                   return_value=MockedRequestsResult(lists_json.read(), api_result_ok)
            ):
                api = ApiCaller(MockedServer(), False, False)
                generator = ListGenerator(api)
                return generator.generate_all()

    def test_list_generator_result_keys(self):
        """
        Tests if all keys in the dictionary generated by ListGenerator.generate_all() are in the ListName enum and
         vice-versa
        """
        lists = self.get_lists()
        # Test if all keys in the response are known
        for k in lists.keys():
            assert k in ListName
        # Test if all known keys are present in the response
        for i in ListName:
            assert i in lists.keys()
        # Test if all lists have at least one element
        for k, v in lists.items():
            self.assertGreater(len(v.list), 0)

    def test_vehicles(self):
        """
        Test if the vehicles section is a subset of the liveries section
        """
        lists = self.get_lists()
        self.assertEqual(
            lists[ListName.vehicles].description,
            "All known vehicles. Each structure contains the vehicle's id, name, (optionally) class and list of all liveries"
        )
        for vehicle in lists[ListName.vehicles].list:
            for livery in vehicle.liveries.list:
                self.assertEqual(livery.vehicle, vehicle)

        assert "McLaren 12C GT3" in [vehicle.name for vehicle in lists[ListName.vehicles].list]
        assert "RWD P20 LMP2" in [vehicle.name for vehicle in lists[ListName.vehicles].list]
