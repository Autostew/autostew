import logging

from autostew_back.plugins import db, laptimes, crash_monitor, motd, db_reader, db_writer, db_enum_writer, clock
from autostew_back.setups import prl_s1_r2_dubai

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('django.db.backends').setLevel(logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)


class Settings:
    host_name = "Host1"
    server_name = "Server1"
    config_file = "/home/joan/.steam/steam/SteamApps/common/Project CARS Dedicated Server/server.cfg"
    api_record_destination = "api_record"
    url = "http://localhost:9000"
    event_poll_period = 10
    full_update_period = 10

    setup_rotation = [prl_s1_r2_dubai]

    plugins = [
        db,
        db_enum_writer,
        db_reader,
        db_writer,
        clock,
        laptimes,
        crash_monitor,
        motd,
    ]

