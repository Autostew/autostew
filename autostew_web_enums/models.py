from django.db import models


class EventDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    attributes = models.TextField(max_length=200)

    def __str__(self):
        return "{}-{}".format(self.type, self.name)


class GameModeDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class TireWearDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class PenaltyDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class FuelUsageDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class AllowedViewsDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class PlayerFlagDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class WeatherDefinition(models.Model):
    name_to_icon = {
        'Random': '<span class="glyphicon glyphicon-question-sign" aria-hidden="true" title="{}"></span>',
        'Hazy': '<i class="wi wi-day-haze" title="{}"></i>',
        'HeavyFogWithRain': '<i class="wi wi-rain-wind" title="{}"></i>',
        'FogWithRain': '<i class="wi wi-day-rain-wind" title="{}"></i>',
        'HeavyFog': '<i class="wi wi-fog" title="{}"></i>',
        'Foggy': '<i class="wi wi-day-fog" title="{}"></i>',
        'ThunderStorm': '<i class="wi wi-thunderstorm" title="{}"></i>',
        'Storm': '<i class="wi wi-day-storm-showers" title="{}"></i>',
        'Rain': '<i class="wi wi-day-rain" title="{}"></i>',
        'LightRain': '<i class="wi wi-day-sleet" title="{}"></i>',
        'Overcast': '<i class="wi wi-day-cloudy-high" title="{}"></i>',
        'HeavyCloud': '<i class="wi wi-cloudy" title="{}"></i>',
        'MediumCloud': '<i class="wi wi-cloud" title="{}"></i>',
        'LightCloud': '<i class="wi wi-day-sunny-overcast" title="{}"></i>',
        'Clear': '<i class="wi wi-day-sunny" title="{}"></i>',
    }
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def get_icon_or_name(self):
        return WeatherDefinition.name_to_icon.get(self.name, self.name).format(self.name)

    def __str__(self):
        return self.name


class DamageDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class SessionFlagDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name


class SessionAttributeDefinition(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class MemberAttributeDefinition(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ParticipantAttributeDefinition(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class LeavingReason(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MemberLoadState(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MemberState(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ParticipantState(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def in_race(self):
        return self.name not in ('DNF', 'Retired', 'Disqualified')


class SessionState(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SessionStage(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SessionPhase(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

