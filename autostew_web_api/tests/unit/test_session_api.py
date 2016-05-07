from rest_framework.test import APIRequestFactory, APITestCase

from autostew_web_session.tests.factories.session_factories import SessionFactory


class SessionApiTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_session_api_no_sessions(self):
        response = self.client.get('/api/sessions?format=json', follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response)
        self.assertEquals(response.data['count'], 0)
        self.assertEquals(response.data['results'], [])

    def test_session_api_one_session(self):
        # create single session first!
        SessionFactory.create()
        response = self.client.get('/api/sessions/?format=json', follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response)
        self.assertEquals(response.data['count'], 1)
        self.assertEquals(len(response.data['results']), 1)

    def test_session_api_one_session_detail(self):
        session = SessionFactory.create()
        response = self.client.get('/api/sessions/%d?format=json' % session.id, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response)
        self.assertEquals(response.data['id'], session.id)
        self.assertEquals(response.data['wetness_path'], session.wetness_path)
        self.assertEquals(response.data['wetness_avg'], session.wetness_avg)
