from unittest.case import skip

from django.test import TestCase

from autostew_web_users.models import SteamUser


class TestElo(TestCase):
    @skip
    def test_rating_transformation(self):
        self.assertEqual(SteamUser._transform_rating(2400), 10 ** 6)
        self.assertEqual(SteamUser._transform_rating(2000), 10 ** 5)

    @skip
    def test_elo_rating_calculation(self):
        self.assertEqual(SteamUser._calculate_new_player_elo_rating(2400, 2000, True, 32), 2403)
        self.assertEqual(SteamUser._calculate_new_player_elo_rating(2000, 2400, False, 32), 1997)
        self.assertEqual(SteamUser._calculate_new_player_elo_rating(2400, 2000, False, 32), 2371)
        self.assertEqual(SteamUser._calculate_new_player_elo_rating(2000, 2400, True, 32), 2029)

    @skip
    def test_minimum_rating(self):
        self.assertEqual(SteamUser._calculate_new_player_elo_rating(0, 0, False, 32), 0)
