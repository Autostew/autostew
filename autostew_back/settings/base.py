import logging

from autostew_back.plugins import db, laptimes, crash_monitor, chat_notifications, db_setup_rotation, db_session_writer, db_enum_writer, clock

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('django.db.backends').setLevel(logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)


class BaseSettings:
    event_poll_period = 1
    full_update_period = 5

    api_record_destination = "api_record"

    plugins = [
        db,
        db_enum_writer,
        db_setup_rotation,
        db_session_writer,
        clock,
        laptimes,
        crash_monitor,
        chat_notifications,
    ]

    api_compatibility = {
        'build_version': [87, 88],
        'lua_version': [301],
        'protocol_version': [135, 136],
    }
