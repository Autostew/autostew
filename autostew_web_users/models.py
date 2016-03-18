from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
class SteamUser(models.Model):
    steam_id = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('users:profile', args=[str(self.steam_id)])


class Steward(models.Model):
    pass
    #user = models.ForeignKey(User) # NOT STEAM USER!