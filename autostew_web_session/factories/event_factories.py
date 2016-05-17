from datetime import datetime
import factory

from autostew_web_enums.factories.enum_factories import EventTypeFactory
from autostew_web_session.models.event import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    type = factory.SubFactory(EventTypeFactory)
    ingame_index = factory.Sequence(lambda n: n)
    raw = ''
    retries_remaining = 2
    handled = False

    @factory.lazy_attribute
    def timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M')
