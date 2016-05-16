import datetime

import factory

from autostew_web_enums.factories.enum_factories import SessionStateFactory, SessionStageFactory, \
    SessionPhaseFactory
from autostew_web_session.factories.server_factories import ServerFactory
from autostew_web_session.factories.session_setup_factories import SessionSetupFactory
from autostew_web_session.models.session import Session


class SessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Session

    parent = None
    server = factory.SubFactory(ServerFactory)
    setup_template = factory.SubFactory(SessionSetupFactory)
    setup_actual = None

    schedule_time = None
    schedule_date = None
    running = False
    finished = False

    max_member_count = 32

    first_snapshot = None

    fastest_lap = None

    is_result = False
    is_final_result = False
    session_state = factory.SubFactory(SessionStateFactory)
    session_stage = factory.SubFactory(SessionStageFactory)
    session_phase = factory.SubFactory(SessionPhaseFactory)
    session_time_elapsed = 0
    session_time_duration = 0
    num_participants_valid = 0
    num_participants_disq = 0
    num_participants_retired = 0
    num_participants_dnf = 0
    num_participants_finished = 0
    current_year = 0
    current_month = 0
    current_day = 0
    current_hour = 0
    current_minute = 0
    rain_density_visual = 0
    wetness_path = 0
    wetness_off_path = 0
    wetness_avg = 0
    wetness_predicted_max = 0
    wetness_max_level = 0
    temperature_ambient = 0
    temperature_track = 0
    air_pressure = 0

    @factory.lazy_attribute
    def start_timestamp(self):
        return datetime.datetime.now

    @factory.lazy_attribute
    def last_update_timestamp(self):
        return datetime.datetime.now

    @factory.lazy_attribute
    def timestamp(self):
        return datetime.datetime.now
