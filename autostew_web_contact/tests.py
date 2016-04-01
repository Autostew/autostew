from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from autostew_web_contact.models import ContactMessage


class TestContact(TestCase):
    def test_contact_page(self):
        response = self.client.get(reverse('contact:contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_post(self):
        response = self.client.post(
            reverse('contact:contact'),
            {
                'name': 'Robert Marley',
                'message': 'One love'
            }
        )
        self.assertRedirects(response, reverse('home:home'))
        contact_messages = ContactMessage.objects.all()
        self.assertEqual(len(contact_messages), 1)
        self.assertEqual(contact_messages[0].name, 'Robert Marley')
        self.assertEqual(contact_messages[0].message, 'One love')
        self.assertEqual(contact_messages[0].email, '')

        response = self.client.post(
            reverse('contact:contact'),
            {
                'name': 'Robert Marley',
                'message': 'One love',
                'email': 'bob@babylon.net'
            }
        )
        self.assertRedirects(response, reverse('home:home'))
        contact_messages = ContactMessage.objects.all()
        self.assertEqual(len(contact_messages), 2)
        self.assertEqual(contact_messages[1].name, 'Robert Marley')
        self.assertEqual(contact_messages[1].message, 'One love')
        self.assertEqual(contact_messages[1].email, 'bob@babylon.net')

        response = self.client.get(reverse('home:home'))
        self.assertNotContains(response, 'unread messages')

        user = User.objects.create_superuser("su", "admin@localhost", "secret")
        user.save()
        self.client.login(username="su", password="secret")

        response = self.client.get(reverse('home:home'))
        self.assertContains(response, 'There are 2 unread messages')

        ContactMessage.objects.all().update(read=True)

        response = self.client.get(reverse('home:home'))
        self.assertNotContains(response, 'unread messages')