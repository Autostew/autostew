import logging

from autostew_back.settings.base import *
from autostew_back.plugins import local_setup_rotation
from autostew_back.tests.test_assets import prl_s4_r2_zolder_casual


server_name = "TestServer"
event_poll_period = 0
full_update_period = 0

setup_rotation = [
    prl_s4_r2_zolder_casual
]

plugins = [db_session_writer]
