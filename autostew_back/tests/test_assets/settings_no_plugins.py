import logging

from autostew_back.settings import Settings as DefaultSettings
from autostew_back.plugins import local_setup_rotation
from autostew_back.tests.test_assets import prl_s4_r2_zolder_casual

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('django.db.backends').setLevel(logging.INFO)
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)


class SettingsWithoutPlugins:
    host_name = "TestHost"
    server_name = "TestServer"
    config_file = "server.cfg"
    url = "http://localhost:9000"
    event_poll_period = 0
    full_update_period = 0

    setup_rotation = [
        prl_s4_r2_zolder_casual
    ]

    plugins = [local_setup_rotation]

    api_compatibility = DefaultSettings.api_compatibility
