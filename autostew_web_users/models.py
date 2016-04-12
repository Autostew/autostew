from django.core.urlresolvers import reverse
from django.db import models

from autostew_web_session import models as session_models


class SteamUser(models.Model):
    class Meta:
        ordering = ['display_name']
    steam_id = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    previous_elo_rating = models.IntegerField(null=True)
    elo_rating = models.IntegerField(null=True)
    safety_rating = models.IntegerField(null=True)
    safety_class = models.ForeignKey('SafetyClass', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('users:profile', args=[str(self.steam_id)])

    def get_safety_rating(self):
        return self.safety_rating

    def get_performance_rating(self):
        return self.elo_rating

    def update_safety_class(self):
        if not SafetyClass.objects.exists():
            return
        if self.safety_class is None:
            self.safety_class = SafetyClass.objects.get(initial_class=True)
        if (
                    self.safety_rating > self.safety_class.drop_from_this_class_threshold and
                    self.safety_class.class_below
        ):
            self.safety_class = self.safety_class.class_below
            self.update_safety_class()
        if (
                    hasattr(self.safety_class, 'class_above') and
                    self.safety_rating < self.safety_class.class_above.raise_to_this_class_threshold
        ):
            self.safety_class = self.safety_class.class_above
            self.update_safety_class()

    def sessions_participated_in(self):
        return session_models.Session.objects.filter(
            id__in=session_models.Session.objects.filter(lap_set__participant__member__steam_user=self).values('id')
         )

    def over_class_kick_impact_threshold(self, crash_magnitude):
        return (self.safety_class and
                self.safety_class.kick_on_impact_threshold and
                crash_magnitude >= self.safety_class.kick_on_impact_threshold)

    def __str__(self):
        return self.display_name


class SafetyClass(models.Model):
    class Meta:
        ordering = ['order']
    order = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    class_below = models.OneToOneField('SafetyClass', null=True, blank=True, related_name='class_above')
    raise_to_this_class_threshold = models.IntegerField()
    drop_from_this_class_threshold = models.IntegerField()
    kick_on_impact_threshold = models.IntegerField(null=True, blank=True)
    initial_class = models.BooleanField(default=False)
    impact_weight = models.IntegerField(default=1)

    def __str__(self):
        return self.name
