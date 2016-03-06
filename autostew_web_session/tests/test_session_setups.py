from django.test import TestCase

from autostew_web_session.models import SessionSetup


def create_session_setup():
    return SessionSetup.objects.create()


# class TrackTests(TestCase):
#
#     def test_can_create_session_setup(self):
#         track = create_session_setup()
#         self.assertNotNone(track)
