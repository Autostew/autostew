from django.core.urlresolvers import reverse
from django.db import models


class SteamUser(models.Model):
    class Meta:
        ordering = ['display_name']
    steam_id = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    previous_elo_rating = models.IntegerField(null=True)
    elo_rating = models.IntegerField(null=True)
    safety_rating = models.IntegerField(null=True)

    def get_absolute_url(self):
        return reverse('users:profile', args=[str(self.steam_id)])

    def get_safety_rating(self):
        return self.safety_rating

    def get_performance_rating(self):
        return self.elo_rating

    def __str__(self):
        return self.display_name
