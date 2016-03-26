import logging

from autostew_back.plugins import db, laptimes, crash_monitor, chat_notifications, db_setup_rotation, db_session_writer, db_enum_writer, clock

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('django.db.backends').setLevel(logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)


class Settings:
    host_name = "Host1"
    server_name = "Server1"
    config_file = "/home/joan/.steam/steam/SteamApps/common/Project CARS Dedicated Server/server.cfg"
    api_record_destination = "api_record"
    url = "http://localhost:9000"
    event_poll_period = 1
    full_update_period = 5

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

