import logging

from autostew_back.tests.test_assets import prl_s4_r2_zolder_casual

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('django.db.backends').setLevel(logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)


class SettingsWithoutPlugins:
    host_name = "TestHost"
    server_name = "TestServer"
    config_file = "server.cfg"
    url = "http://localhost:9000"
    event_poll_period = 1
    full_update_period = 5

    setup_rotation = [
        prl_s4_r2_zolder_casual
    ]

    plugins = []
