import datetime
import factory

from autostew_web_session.models.server import Server
from autostew_web_session.tests.factories.session_setup_factories import SessionSetupFactory


class ServerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Server

    name = factory.Sequence(lambda n: 'Server%d' % n)
    contact = factory.LazyAttribute(lambda o: '%s@example.org' % o.api_username)
    owner = None

    api_url = factory.LazyAttribute(lambda o: 'http://%s:%s@%s:%d/' % (o.api_username, o.api_password,
                                                                       o.api_address, o.api_port))

    api_username = factory.faker.faker.Factory.create().name()
    api_password = factory.faker.faker.Factory.create().password()
    api_address = "127.0.0.1"
    api_port = 9000

    back_verified = False
    back_enabled = False
    back_reconnect = True
    back_kicks = True
    back_crash_points_limit = 4000
    back_crash_points_limit_ban_seconds = 0
    back_safety_rating = True
    back_performance_rating = True
    back_custom_motd = "Custom message"
    back_minimal_safety_class = None

    setup_rotation_index = 0
    #setup_rotation = None

    #setup_queue = factory.SubFactory(SessionSetupFactory)

    running = False
    current_session = None
    last_ping = None
    average_player_latency = None
    joinable_internal = False
    state = None
    session_state = None
    lobby_id = 0
    max_member_count = 0

    is_up = False

    @factory.lazy_attribute
    def time_since_last_ping(self):
        return datetime.datetime.now
