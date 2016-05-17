from django.core.urlresolvers import reverse
from django.db import models
from math import floor

from autostew_web_session.models import session as session_models


class SteamUser(models.Model):
    per_km_safety_multiplier = 0.995
    initial_safety_rating = 10000
    elo_k = 5
    initial_elo_rating = 1000
    minimum_elo_rating = 0

    class Meta:
        ordering = ['-elo_rating', 'display_name']
    steam_id = models.CharField(max_length=100, db_index=True)
    display_name = models.CharField(max_length=100)
    previous_elo_rating = models.IntegerField(null=True)
    elo_rating = models.IntegerField(null=True)
    safety_rating = models.IntegerField(null=True)
    safety_class = models.ForeignKey('SafetyClass', null=True, blank=True)
    total_distance = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('users:profile', args=[str(self.steam_id)])

    def get_safety_rating(self):
        return self.safety_rating

    def get_performance_rating(self):
        return self.elo_rating

    def get_performance_rating_diff(self):
        if self.elo_rating and self.previous_elo_rating:
            return self.elo_rating - self.previous_elo_rating
        return None

    def get_kms(self):
        return floor(self.total_distance / 1000)

    def push_elo_rating(self):
        if self.elo_rating is None:
            self.elo_rating = self.initial_elo_rating
        self.previous_elo_rating = self.elo_rating
        self.save()

    def update_elo_rating(self, opponent, won: float):
        if won is None:
            return
        win_expectation = self.transformed_previous_rating / (opponent.transformed_previous_rating + self.transformed_previous_rating)
        self.elo_rating += self.elo_k * (won - win_expectation)
        if self.elo_rating < self.minimum_elo_rating:
            self.elo_rating = self.minimum_elo_rating
        self.save()

    @property
    def transformed_rating(self):
        return 10 ** (self.elo_rating / 400)

    @property
    def transformed_previous_rating(self):
        return 10 ** (self.elo_rating / 400)

    def add_crash_points(self, points):
        if self.safety_rating is None:
            self.safety_rating = self.initial_safety_rating
        self.safety_rating += points
        result = self.update_safety_class()
        self.save()
        return result

    def add_distance(self, distance):
        if self.safety_rating is None:
            self.safety_rating = self.initial_safety_rating
        self.total_distance += distance
        self.safety_rating *= self.per_km_safety_multiplier**(distance/1000)
        result = self.update_safety_class()
        self.save()
        return result

    def update_safety_class(self):
        if not SafetyClass.objects.exists():
            return False
        if self.safety_class is None:
            self.safety_class = SafetyClass.objects.get(initial_class=True)
            self.save()
            return True
        if self.safety_rating is None:
            self.safety_rating = self.initial_safety_rating
        if (
                    self.safety_rating > self.safety_class.drop_from_this_class_threshold and
                    self.safety_class.class_below
        ):
            self.safety_class = self.safety_class.class_below
            self.update_safety_class()
            return True
        if (
                    hasattr(self.safety_class, 'class_above') and
                    self.safety_rating < self.safety_class.class_above.raise_to_this_class_threshold
        ):
            self.safety_class = self.safety_class.class_above
            self.update_safety_class()
            return True
        return False

    def sessions_participated_in(self):
        return session_models.Session.objects.filter(
            id__in=session_models.Session.objects.filter(lap_set__participant__member__steam_user=self).values('id')
         ).reverse()

    def over_class_kick_impact_threshold(self, crash_magnitude):
        return (self.safety_class and
                self.safety_class.kick_on_impact_threshold and
                crash_magnitude >= self.safety_class.kick_on_impact_threshold)

    def __str__(self):
        return self.display_name


class SafetyClass(models.Model):
    class Meta:
        ordering = ['order']
    order = models.IntegerField(db_index=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    class_below = models.OneToOneField('SafetyClass', null=True, blank=True, related_name='class_above')
    raise_to_this_class_threshold = models.IntegerField()
    drop_from_this_class_threshold = models.IntegerField()
    kick_on_impact_threshold = models.IntegerField(null=True, blank=True)
    initial_class = models.BooleanField(default=False)
    impact_weight = models.IntegerField(default=1)
    label_class = models.CharField(max_length=20, default="default")

    def __str__(self):
        return self.name
