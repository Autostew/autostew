from unittest import TestCase

from autostew_back.event_handlers.session_start import HandleSessionStart
from autostew_web_session.factories.event_factories import EventFactory


class TestSessionStart(TestCase):

    def setUp(self):
        pass

    def test_can_consume(self):
        event = EventFactory.create()
        #self.assertEquals(True, HandleSessionStart.can_consume(None, event))
