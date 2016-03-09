import logging

from autostew_back.plugins import laptimes, crash_monitor, motd, db, db_reader, db_writer, db_enum_writer

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('django.db.backends').setLevel(logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.DEBUG)


class Settings:
    host_name = "Host1"
    server_name = "Server1"
    config_file = "/home/joan/.steam/steam/SteamApps/common/Project CARS Dedicated Server/server.cfg"
    url = "http://localhost:9000"
    event_poll_period = 1
    full_update_period = 5

    setup_rotation = []

    plugins = [
        db,
        db_reader,
        db_enum_writer,
        db_writer,
        laptimes,
        crash_monitor,
        motd,
    ]

