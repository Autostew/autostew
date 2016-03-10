import logging

from autostew_back.plugins import db, laptimes, crash_monitor, motd, db_reader, db_writer, db_enum_writer
from autostew_back.setups import prl_s4_r2_zolder_casual

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('django.db.backends').setLevel(logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.DEBUG)


class Settings:
    host_name = "Host1"
    server_name = "Server1"
    config_file = "/home/joan/.steam/steam/SteamApps/common/Project CARS Dedicated Server/server.cfg"
    api_record_destination = "api_record"
    url = "http://localhost:9000"
    event_poll_period = 1
    full_update_period = 5

    setup_rotation = [
        prl_s4_r2_zolder_casual
    ]

    plugins = [
        db,
        db_reader,
        db_enum_writer,
        db_writer,
        laptimes,
        crash_monitor,
        motd,
    ]

