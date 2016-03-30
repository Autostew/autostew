
from django.test import TestCase
from autostew_back.plugins import db_elo_rating


class TestElo(TestCase):
    def test_rating_transformation(self):
        self.assertEqual(db_elo_rating.calculate_transformed_rating(2400), 10**6)
        self.assertEqual(db_elo_rating.calculate_transformed_rating(2000), 10**5)

    def test_elo_rating_calculation(self):
        self.assertEqual(db_elo_rating.calculate_new_elo_rating(2400, 2000, True, 32), 2402)
        self.assertEqual(db_elo_rating.calculate_new_elo_rating(2000, 2400, False, 32), 1997)
        self.assertEqual(db_elo_rating.calculate_new_elo_rating(2400, 2000, False, 32), 2370)
        self.assertEqual(db_elo_rating.calculate_new_elo_rating(2000, 2400, True, 32), 2029)
