from django.test import TestCase


class SessionApiTests(TestCase):
    def test_session_api(self):
        resp = self.client.get('/api/sessions')
        self.assertEqual(resp.status_code, 301)
