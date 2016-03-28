from django.test import TestCase


class TestHomePage(TestCase):
    def test_home_page(self):
        """
        Tests if the homepage exists
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
