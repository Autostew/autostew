"""
Calculates Elo ratings for drivers once a race is finished
"""
name = 'Elo rating'


def calculate_new_elo_rating(player_rating: int, opponent_rating: int, won: bool, k: int):
    transformed_rating = calculate_transformed_rating(player_rating)
    opponent_transformed_rating = calculate_transformed_rating(opponent_rating)
    win_expectation = transformed_rating / (transformed_rating + opponent_transformed_rating)
    new_rating = player_rating + k * (int(won) - win_expectation)
    return int(new_rating)


def calculate_transformed_rating(player_rating):
    return 10 ** (player_rating / 400)
