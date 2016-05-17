import random
import factory

import autostew_web_enums.models


class EventDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default event'
    type = 'default type'
    description = factory.Faker('text')
    attributes = 'abc'


class GameModeDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.GameModeDefinition

    name = 'Default game mode'
    ingame_id = random.randint(-9999, 9999)


class TireWearDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.TireWearDefinition

    name = 'x3'
    ingame_id = random.randint(-9999, 9999)


class PenaltyDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.PenaltyDefinition

    name = 'Default penalty'
    ingame_id = random.randint(-9999, 9999)


class FuelUsageDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.FuelUsageDefinition

    name = 'Default fuel usage'
    ingame_id = random.randint(-9999, 9999)


class AllowedViewsDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.AllowedViewsDefinition

    name = 'Default allowed views'
    ingame_id = random.randint(-9999, 9999)


class PlayerFlagDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.PlayerFlagDefinition

    name = 'Default player flag'
    ingame_id = random.randint(-9999, 9999)


class WeatherDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.WeatherDefinition

    name = 'Default weather'
    ingame_id = random.randint(-9999, 9999)


class PrivacyDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.PrivacyDefinition

    name = 'Default damage'
    ingame_id = random.randint(-9999, 9999)


class DamageDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.DamageDefinition

    name = 'Default damage'
    ingame_id = random.randint(-9999, 9999)


class SessionFlagDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.SessionFlagDefinition

    name = 'Default session flag'
    ingame_id = random.randint(-9999, 9999)


class SessionAttributeDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.SessionAttributeDefinition

    name = 'Default session attribute'
    type = 'Default type'
    access = 'Default access'
    description = factory.Faker('text')


class MemberAttributeDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = autostew_web_enums.models.MemberAttributeDefinition

    name = 'Default member attribute'
    type = 'Default type'
    access = 'Default access'
    description = factory.Faker('text')


class ParticipantAttributeDefinitionFactory(factory.django.DjangoModelFactory):
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