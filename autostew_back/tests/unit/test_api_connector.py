from unittest import mock
from unittest.mock import Mock

import requests
from django.test import TestCase

from autostew_back.ds_api.api_connector import ApiConnector
from autostew_web_enums.models import DamageDefinition

simple_translation = [
    {'model_field': 'practice1_length', 'api_field': 'Practice1Length'}
]

enum_translation = [
    {'model_field': 'damage', 'api_field': 'DamageType', 'enum_model': DamageDefinition},
]

flag_translation = [
    {'model_field': 'one', 'flag': 1, 'api_field': 'Flags'},
    {'model_field': 'two', 'flag': 2, 'api_field': 'Flags'},
]


class NoApi:
    def _call(self):
        pass


class FakeModel:
    def __init__(self):
        self.practice1_length = None
        self.damage = None
        self.one = None
        self.two = None


class TestApiConnector(TestCase):
    def setUp(self):
        pass

    def test_simple_connector_pull(self):
        api_result = {'Practice1Length': 'foo'}
        fake_model = FakeModel()
        translator = ApiConnector(NoApi(), fake_model, simple_translation)
        translator.pull_from_game(api_result)
        self.assertEqual(fake_model.practice1_length, api_result['Practice1Length'])

    def test_simple_connector_push(self):
        api = NoApi
        api._call = Mock(return_value=None)
        fake_model = FakeModel()
        fake_model.practice1_length = 'foo'
        translator = ApiConnector(api, fake_model, simple_translation)
        translator.push_to_game('type')
        api._call.assert_called_once_with(
            'session/set_attributes',
            params={'type_Practice1Length': 'foo'}
        )

    def test_connector_pull_with_enum(self):
        api_result = {'DamageType': '2'}
        DamageDefinition.objects.create(name='foo', ingame_id=1)
        expected = DamageDefinition.objects.create(name='bar', ingame_id=2)
        fake_model = FakeModel()
        translator = ApiConnector(NoApi(), fake_model, enum_translation)
        translator.pull_from_game(api_result)
        self.assertEqual(fake_model.damage, expected)

    def test_connector_push_with_enum(self):
        api = NoApi
        api._call = Mock(return_value=None)
        fake_model = FakeModel()
        fake_model.damage = DamageDefinition.objects.create(name='bar', ingame_id=2)
        translator = ApiConnector(api, fake_model, enum_translation)
        translator.push_to_game('type')
        api._call.assert_called_once_with(
            'session/set_attributes',
            params={'type_DamageType': 2}
        )

    def test_connector_pull_flag_empty(self):
        api_result = {'Flags': '0'}
        fake_model = FakeModel()
        translator = ApiConnector(NoApi(), fake_model, flag_translation)
        translator.pull_from_game(api_result)
        self.assertEqual(fake_model.one, False)
        self.assertEqual(fake_model.two, False)

    def test_connector_pull_flag_one(self):
        api_result = {'Flags': '2'}
        fake_model = FakeModel()
        translator = ApiConnector(NoApi(), fake_model, flag_translation)
        translator.pull_from_game(api_result)
        self.assertEqual(fake_model.one, False)
        self.assertEqual(fake_model.two, True)

    def test_connector_pull_flag_multiple(self):
        api_result = {'Flags': '3'}
        fake_model = FakeModel()
        translator = ApiConnector(NoApi(), fake_model, flag_translation)
        translator.pull_from_game(api_result)
        self.assertEqual(fake_model.one, True)
        self.assertEqual(fake_model.two, True)

    def test_connector_push_flag_empty(self):
        api = NoApi
        api._call = Mock(return_value=None)
        fake_model = FakeModel()
        fake_model.one = False
        fake_model.two = False
        translator = ApiConnector(api, fake_model, flag_translation)
        translator.push_to_game('type')
        api._call.assert_called_once_with(
            'session/set_attributes',
            params={'type_Flags': 0}
        )

    def test_connector_push_flag_one(self):
        api = NoApi
        api._call = Mock(return_value=None)
        fake_model = FakeModel()
        fake_model.one = True
        fake_model.two = False
        translator = ApiConnector(api, fake_model, flag_translation)
        translator.push_to_game('type')
        api._call.assert_called_once_with(
            'session/set_attributes',
            params={'type_Flags': 1}
        )

    def test_connector_push_flag_multiple(self):
        api = NoApi
        api._call = Mock(return_value=None)
        fake_model = FakeModel()
        fake_model.one = True
        fake_model.two = True
        translator = ApiConnector(api, fake_model, flag_translation)
        translator.push_to_game('type')
        api._call.assert_called_once_with(
            'session/set_attributes',
            params={'type_Flags': 3}
        )
