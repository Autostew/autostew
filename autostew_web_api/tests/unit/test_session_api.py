from django.test import TestCase


class SessionApiTests(TestCase):
    def test_session_api_no_sessions(self):
        resp = self.client.get('/api/sessions')
        self.assertEqual(resp.status_code, 301)

    def test_session_api_one_session(self):
        resp = self.client.get('/api/sessions/1')
        self.assertEqual(resp.status_code, 301)
