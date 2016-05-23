from django.test import TestCase

from autostew_back.event_handlers.session_start import HandleSessionStart
from autostew_web_enums.models import SessionState, EventType
from autostew_web_session.factories.event_factories import EventFactory


class TestSessionStart(TestCase):
    def test_can_consume_when_state_changed_to_lobby(self):
        event = EventFactory.create()
        event.type.name = EventType.state_changed
        event.new_session_state = SessionState.lobby

        self.assertTrue(HandleSessionStart.can_consume(None, event))

    def test_can_consume_when_session_gets_created(self):
        event = EventFactory.create()
        event.type.name = EventType.session_created

        self.assertTrue(HandleSessionStart.can_consume(None, event))

    def test_consume(self):
        # nothing to test here. Should be tested by server unit tests
        pass
