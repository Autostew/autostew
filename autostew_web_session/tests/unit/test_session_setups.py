from django.test import TestCase

from autostew_web_session.tests.factories.session_setup_factories import SessionSetupFactory


class TrackTests(TestCase):
    def test_can_create_session_setup(self):
        track = SessionSetupFactory()
        self.assertIsNotNone(track)
