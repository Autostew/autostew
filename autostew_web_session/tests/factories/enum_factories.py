import random
import factory

import autostew_web_enums.models


class EventFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default event'
    type = 'default type'
    description = factory.Faker('text')
    attributes = 'abc'


class GameModeFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default game mode'
    ingame_id = random.randint(-9999, 9999)


class TireWearFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'x3'
    ingame_id = random.randint(-9999, 9999)


class PenaltyFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default penalty'
    ingame_id = random.randint(-9999, 9999)


class FuelUsageFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default fuel usage'
    ingame_id = random.randint(-9999, 9999)


class AllowedViewsFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default allowed views'
    ingame_id = random.randint(-9999, 9999)


class PlayerFlagFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default player flag'
    ingame_id = random.randint(-9999, 9999)


class WeatherFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default weather'
    ingame_id = random.randint(-9999, 9999)


class DamageFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default damage'
    ingame_id = random.randint(-9999, 9999)


class SessionFlagFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default session flag'
    ingame_id = random.randint(-9999, 9999)


class SessionAttributeFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default session attribute'
    type = 'Default type'
    access = 'Default access'
    description = factory.Faker('text')


class MemberAttributeFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default member attribute'
    type = 'Default type'
    access = 'Default access'
    description = factory.Faker('text')


class ParticipantAttributeFactory(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default participant attribute'
    type = 'Default type'
    access = 'Default access'
    description = factory.Faker('text')


class EventType(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default event type'


class LeavingReason(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default leaving reason'


class MemberLoadState(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default member load state'


class MemberState(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default member state'


class ParticipantState(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default participant state'


class SessionState(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default session state'


class SessionStage(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default session stage'


class SessionPhase(factory.Factory):
    class Meta:
        model = autostew_web_enums.models.EventDefinition

    name = 'Default session phase'
