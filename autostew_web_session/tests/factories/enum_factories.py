import random

import factory

import autostew_web_enums.models


class EventFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    attributes = models.TextField(max_length=200)


class GameModeFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = factory.Faker('name')
    ingame_id = random.randint(-9999, 9999)


class TireWearFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')


class PenaltyFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')


class FuelUsageFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')


class AllowedViewsFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')


class PlayerFlagFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')


class WeatherFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')


class DamageFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')


class SessionFlagFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50, unique=True)
    ingame_id = models.IntegerField(help_text='pCars internal ID')


class SessionAttributeFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class MemberAttributeFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class ParticipantAttributeFactory(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    access = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class EventType(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)


class LeavingReason(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)


class MemberLoadState(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)


class MemberState(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)


class ParticipantState(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)


class SessionState(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)


class SessionStage(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)


class SessionPhase(factory.Factory):
    class meta:
        model = autostew_web_enums.models.EventDefinition

    name = models.CharField(max_length=50)
