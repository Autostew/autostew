"""
Calculates Elo ratings for drivers once a race is finished
"""
from autostew_web_session.models import Session

initial_rating = 100


def update_ratings_after_race_end(session: Session):
    _push_ratings(session)
    for member in session.member_set.all():
        for opponent in session.member_set.all():
            if member is opponent:
                continue
            #if
            #member.elo_rating = _calculate_new_player_elo_rating(
            #    member.previous_elo_rating,
            #    opponent.previous_elo_rating,
            #    member.
            #)


def _push_ratings(session: Session):
    for member in session.member_set.all():
        member.steam_user.previous_elo_rating = member.steam_user.elo_rating
        member.save()


def _calculate_new_player_elo_rating(player_rating: int, opponent_rating: int, won: bool, k: int):
    transformed_rating = _transform_rating(player_rating)
    opponent_transformed_rating = _transform_rating(opponent_rating)
    win_expectation = transformed_rating / (transformed_rating + opponent_transformed_rating)
    new_rating = player_rating + k * (int(won) - win_expectation)
    return max(round(new_rating), 0)


def _transform_rating(player_rating):
    if player_rating is None:
        player_rating = initial_rating
    return 10 ** (player_rating / 400)
