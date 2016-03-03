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
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class TireWearDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class PenaltyDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class FuelUsageDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class AllowedViewsDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class PlayerFlagDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class WeatherDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class DamageDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

    def __str__(self):
        return self.name


class SessionFlagDefinition(models.Model):
    name = models.CharField(max_length=50, unique=True)
    id = models.IntegerField(primary_key=True, help_text='pCars internal ID')

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
