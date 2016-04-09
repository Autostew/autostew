"""
Calculates Elo ratings for drivers once a race is finished
"""
from autostew_web_session.models.models import Session
from autostew_web_session.models.member import Member

minimum_rating = 0

initial_rating = 1000
default_k = 5


def update_ratings_after_race_end(session: Session):
    if not session.get_members_who_finished_race():
        return
    _push_ratings(session)
    for member in session.get_members_who_participated():
        member.steam_user.refresh_from_db()
        for opponent in session.get_members_who_participated():
            if member == opponent:
                continue
            member.steam_user.elo_rating += _calculate_elo_rating_delta(
                member.steam_user.previous_elo_rating,
                opponent.steam_user.previous_elo_rating,
                _versus_result(session, member, opponent),
                default_k
            )
            member.steam_user.save()


def _versus_result(session: Session, member: Member, opponent: Member) -> float:
    if not session.get_members_who_finished_race():
        return None
    member_stayed = member in session.get_members_who_finished_race()
    opponent_stayed = opponent in session.get_members_who_finished_race()

    if not member_stayed and not opponent_stayed:
        return 0.5
    if member_stayed and not opponent_stayed:
        return 1
    if opponent_stayed and not member_stayed:
        return 0
    if member_stayed and opponent_stayed:
        if member.finishing_position() < opponent.finishing_position():
            return 1
        else:
            return 0


def _push_ratings(session: Session):
    for member in session.member_set.all():
        if member.steam_user.elo_rating is None:
            member.steam_user.elo_rating = initial_rating
        member.steam_user.previous_elo_rating = member.steam_user.elo_rating
        member.steam_user.save()


def _calculate_new_player_elo_rating(player_rating: int, opponent_rating: int, won: float, k: int):
    return max(minimum_rating, player_rating + _calculate_elo_rating_delta(player_rating, opponent_rating, won, k))


def _calculate_elo_rating_delta(player_rating: int, opponent_rating: int, won: float, k: int):
    if won is None:
        return player_rating
    transformed_rating = _transform_rating(player_rating)
    opponent_transformed_rating = _transform_rating(opponent_rating)
    win_expectation = transformed_rating / (transformed_rating + opponent_transformed_rating)
    new_rating = player_rating + k * (won - win_expectation)
    return round(new_rating - player_rating)


def _transform_rating(player_rating):
    return 10 ** (player_rating / 400)
