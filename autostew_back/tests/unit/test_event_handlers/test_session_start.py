from unittest import TestCase

from autostew_back.event_handlers.session_start import HandleSessionStart


class TestSessionStart(TestCase):

    def setUp(self):
        pass

    def test_can_consume(self):
        self.assertEquals(True, HandleSessionStart.can_consume(None, None))
