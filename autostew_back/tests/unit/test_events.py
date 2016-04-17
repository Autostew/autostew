import json
from unittest import mock

import requests
from django.test import TestCase

from autostew_back.ds_api.event import event_factory, BaseEvent, EventType, PlayerJoinedEvent, MemberEvent, \
    StateChangedEvent
from autostew_back.ds_api.mocked_api import FakeApi
from autostew_back.tests.test_assets import settings_no_plugins
from autostew_back.tests.unit.test_plugin_db_writer import TestDBWriter
from autostew_web_enums.models import SessionState
from autostew_web_session.models.server import Server


class FakePlugin:
    name = "Fake Plugin"


class TestEvents(TestCase):
    def test_plugin_inits(self):
        has_done_init = False
        has_done_env_init = False

        fake_plugin = FakePlugin()

        def init(server):
            nonlocal has_done_init
            has_done_init = True
        fake_plugin.init = init

        def env_init(server):
            nonlocal has_done_env_init
            has_done_env_init = True
        fake_plugin.env_init = env_init

        api = FakeApi()
        settings_no_plugins.plugins = [fake_plugin]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = TestDBWriter.make_test_server()
            self.assertFalse(has_done_init)
            self.assertFalse(has_done_env_init)
            server.back_start(settings_no_plugins, False)
            self.assertTrue(has_done_init)
            self.assertFalse(has_done_env_init)
            server.back_start(settings_no_plugins, True)
            self.assertTrue(has_done_init)
            self.assertTrue(has_done_env_init)
            self.assertEqual(server.api.event_offset, 0)

    def test_plugin_tick(self):
        tick_count = 0
        event_count = 0

        fake_plugin = FakePlugin()

        def tick(server):
            nonlocal tick_count
            tick_count += 1
        fake_plugin.tick = tick

        def event(server, event):
            nonlocal event_count
            event_count += 1
        fake_plugin.event = event

        api = FakeApi()
        settings_no_plugins.plugins = [fake_plugin]
        with mock.patch.object(requests, 'get', api.fake_request):
            server = TestDBWriter.make_test_server()
            self.assertEqual(tick_count, 0)
            self.assertEqual(event_count, 0)
            server.back_start(settings_no_plugins, False)
            self.assertEqual(tick_count, 0)
            self.assertEqual(event_count, 0)
            server.back_poll_loop(only_one_run=True)
            self.assertEqual(tick_count, 1)
            self.assertEqual(event_count, 0)
            server.back_poll_loop(only_one_run=True)
            self.assertEqual(tick_count, 2)
            self.assertEqual(event_count, 0)

    def test_plugin_events(self):
        event_count = 0
        expected_event_types = [
            EventType.session_created,
            EventType.player_joined,
            EventType.authenticated,
            EventType.state_changed
        ]
        fake_plugin = FakePlugin()

        def event(server, event):
            nonlocal event_count, expected_event_types
            self.assertEqual(event.type, expected_event_types[event_count])
            event_count += 1
        fake_plugin.event = event

        api = FakeApi()
        api.events_result = 'autostew_back/tests/test_assets/events_after_one_player_joined.json'
        settings_no_plugins.plugins = [fake_plugin]
        server = TestDBWriter.make_test_server()
        with mock.patch.object(requests, 'get', api.fake_request):
            self.assertEqual(event_count, 0)
            server.back_start(settings_no_plugins, False)
            self.assertEqual(event_count, 0)
            server.back_poll_loop(only_one_run=True)
            self.assertEqual(event_count, 4)

    def test_event_factory(self):
        api = FakeApi('autostew_back/tests/test_assets/session_after_one_player_joined.json')
        with mock.patch.object(requests, 'get', api.fake_request):
            server = TestDBWriter.make_test_server()
            server.back_start(settings_no_plugins, False)
            with open('autostew_back/tests/test_assets/events_after_one_player_joined.json') as f:
                event_json = json.load(f)

                session_created_event = event_factory(event_json['response']['events'][0], server)
                self.assertIsInstance(session_created_event, BaseEvent)
                self.assertEqual(session_created_event.index, 0)
                self.assertEqual(session_created_event.type, EventType.session_created)

                player_joined_event = event_factory(event_json['response']['events'][1], server)
                self.assertIsInstance(player_joined_event, PlayerJoinedEvent)
                self.assertIsInstance(player_joined_event, MemberEvent)
                self.assertEqual(player_joined_event.index, 1)
                self.assertEqual(player_joined_event.type, EventType.player_joined)
                self.assertEqual(player_joined_event.steam_id, player_joined_event.member.steam_id.get())
                self.assertEqual(player_joined_event.raw['refid'], player_joined_event.member.refid.get())

                authenticated_event = event_factory(event_json['response']['events'][2], server)
                self.assertIsInstance(authenticated_event, MemberEvent)
                self.assertEqual(authenticated_event.type, EventType.authenticated)
                self.assertEqual(authenticated_event.raw['refid'], authenticated_event.member.refid.get())

                state_changed_event = event_factory(event_json['response']['events'][3], server)
                self.assertIsInstance(state_changed_event, StateChangedEvent)
                self.assertEqual(state_changed_event.type, EventType.state_changed)
                self.assertEqual(state_changed_event.previous_state, SessionState.none)
                self.assertEqual(state_changed_event.new_state, SessionState.lobby)
