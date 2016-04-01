"""
Calculates safety ratings
"""

last_lap_weight = 1/50
initial_safety_rating = 3000


def lap_completed(user):
    if user.safety_rating is None:
        user.safety_rating = initial_safety_rating
    user.safety_rating *= (1-last_lap_weight)
    user.update_safety_class()
    user.save()


def impact(user, points: int):
    if user.safety_rating is None:
        user.safety_rating = initial_safety_rating
    user.safety_rating += points
    user.update_safety_class()
    user.save()
