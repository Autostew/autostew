#!/usr/bin/python3
import logging

import requests
from autostew_back.settings import Settings

logging.getLogger().setLevel(logging.DEBUG)

input("Run this only with a running DS with HTTP API enabled and no game ever started on it. Press enter to continue")

with open('autostew_back/tests/test_assets/version.json', 'w') as file_output:
    result = requests.get(Settings.url + '/api/version')
    file_output.write(result.text)

with open('autostew_back/tests/test_assets/help.json', 'w') as file_output:
    result = requests.get(Settings.url + '/api/help')
    file_output.write(result.text)

with open('autostew_back/tests/test_assets/lists.json', 'w') as file_output:
    result = requests.get(Settings.url + '/api/list/all')
    file_output.write(result.text)

with open('autostew_back/tests/test_assets/empty_session.json', 'w') as file_output:
    result = requests.get(Settings.url + '/api/session/status?attributes=1&members=1&participants=1')
    file_output.write(result.text)