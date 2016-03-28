from django.test import TestCase
from django.core.urlresolvers import reverse

from autostew_web_session.models import Track


def create_track(ingame_id=-1337, name='testtrack', grid_size=42):
    return Track.objects.create(ingame_id=ingame_id, name=name, grid_size=grid_size)


class TrackTests(TestCase):

    def test_can_create_track(self):
        track = create_track()
        self.assertEqual(-1337, track.ingame_id)
        self.assertEqual('testtrack', track.name)
        self.assertEqual(42, track.grid_size)


class TrackIndexViewTests(TestCase):
    def test_index_view_with_no_tracks(self):
        """
        If no tracks exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('session:tracks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tracks are available")
        self.assertQuerysetEqual(response.context['track_list'], [])

    def test_index_view_with_one_track(self):
        """
        Should list that track
        """
        track = create_track()
        response = self.client.get(reverse('session:tracks', args=()))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, track.name)
        self.assertQuerysetEqual(response.context['track_list'], ['<Track: testtrack>'])


class TrackDetailViewTests(TestCase):
    def test_detail_view_of_a_track(self):
        """
        Should list the details of that track
        """
        track = create_track()
        response = self.client.get(reverse('session:track', args=(track.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, track.name)
        self.assertContains(response, track.grid_size)
        self.assertEqual(response.context['track'], track)
