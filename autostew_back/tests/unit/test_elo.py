from django.test import TestCase

from autostew_back.plugins.db_session_writer_libs import db_elo_rating


class TestElo(TestCase):
    def test_rating_transformation(self):
        self.assertEqual(db_elo_rating._transform_rating(2400), 10 ** 6)
        self.assertEqual(db_elo_rating._transform_rating(2000), 10 ** 5)

    def test_elo_rating_calculation(self):
        self.assertEqual(db_elo_rating._calculate_new_player_elo_rating(2400, 2000, True, 32), 2403)
        self.assertEqual(db_elo_rating._calculate_new_player_elo_rating(2000, 2400, False, 32), 1997)
        self.assertEqual(db_elo_rating._calculate_new_player_elo_rating(2400, 2000, False, 32), 2371)
        self.assertEqual(db_elo_rating._calculate_new_player_elo_rating(2000, 2400, True, 32), 2029)

    def test_minimum_rating(self):
        self.assertEqual(db_elo_rating._calculate_new_player_elo_rating(0, 0, False, 32), 0)
