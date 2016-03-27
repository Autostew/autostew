import importlib
import os
import pkgutil
from unittest import mock

import requests
from django.test import TestCase

from autostew_back import setups
from autostew_back.gameserver.mocked_api import FakeApi
from autostew_back.gameserver.server import Server
from autostew_back.plugins import local_setup_rotation
from autostew_back.tests.test_assets.settings_no_plugins import SettingsWithoutPlugins


class TestSetups(TestCase):
    def test_setups_basic(self):
        """
        Does a very basic test on the existing modules (just try loading them)
        """
        api = FakeApi()
        settings = SettingsWithoutPlugins()
        setups_path = os.path.dirname(setups.__file__)
        modules = [name for _, name, _ in pkgutil.iter_modules([setups_path])]
        for setup_module in modules:
            setup = importlib.import_module('autostew_back.setups.{}'.format(setup_module))
            settings.setup_rotation = [setup]
            with mock.patch.object(requests, 'get', api.fake_request):
                server = Server(settings, True)
                local_setup_rotation.load_next_setup(server)
