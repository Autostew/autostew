import logging

from autostew_back.settings.base import *
from autostew_back.plugins import local_setup_rotation
from autostew_back.tests.test_assets import no_setup

server_name = "TestServer"
event_poll_period = 0
full_update_period = 0

setup_rotation = [
    no_setup
]

plugins = [local_setup_rotation]
