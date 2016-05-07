import random
import factory

import autostew_web_enums.models


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default event'
    type = 'default type'
    description = factory.Faker('text')
    attributes = 'abc'


class GameModeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.GameModeDefinition

    name = 'Default game mode'
    ingame_id = random.randint(-9999, 9999)


class TireWearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.TireWearDefinition

    name = 'x3'
    ingame_id = random.randint(-9999, 9999)


class PenaltyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.PenaltyDefinition

    name = 'Default penalty'
    ingame_id = random.randint(-9999, 9999)


class FuelUsageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.FuelUsageDefinition

    name = 'Default fuel usage'
    ingame_id = random.randint(-9999, 9999)


class AllowedViewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.AllowedViewsDefinition

    name = 'Default allowed views'
    ingame_id = random.randint(-9999, 9999)


class PlayerFlagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.PlayerFlagDefinition

    name = 'Default player flag'
    ingame_id = random.randint(-9999, 9999)


class WeatherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.WeatherDefinition

    name = 'Default weather'
    ingame_id = random.randint(-9999, 9999)


class PrivacyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.PrivacyDefinition

    name = 'Default damage'
    ingame_id = random.randint(-9999, 9999)


class DamageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.DamageDefinition

    name = 'Default damage'
    ingame_id = random.randint(-9999, 9999)


class SessionFlagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.SessionFlagDefinition

    name = 'Default session flag'
    ingame_id = random.randint(-9999, 9999)


class SessionAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.SessionAttributeDefinition

    name = 'Default session attribute'
    type = 'Default type'
    access = 'Default access'
    description = factory.Faker('text')


class MemberAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.MemberAttributeDefinition

    name = 'Default member attribute'
    type = 'Default type'
    access = 'Default access'
    description = factory.Faker('text')


class ParticipantAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.ParticipantAttributeDefinition

    name = 'Default participant attribute'
    type = 'Default type'
    access = 'Default access'
    description = factory.Faker('text')


class EventTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.EventType

    name = 'Default event type'


class LeavingReasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.LeavingReason

    name = 'Default leaving reason'


class MemberLoadStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.MemberLoadState

    name = 'Default member load state'


class MemberStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.MemberState

    name = 'Default member state'


class ParticipantStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.ParticipantState

    name = 'Default participant state'


class SessionStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.SessionState

    name = 'Default session state'


class SessionStageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.SessionStage

    name = 'Default session stage'


class SessionPhaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.SessionPhase

    name = 'Default session phase'
