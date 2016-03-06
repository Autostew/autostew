#!/usr/bin/python3

import requests
from autostew_back.settings import Settings
import autostew_back

input("Run thsi only with a running DS with HTTP API enabled and no game ever started on it. Press enter to continue")

with open('autostew_back/tests/test_assets/lists.json', 'w') as list_output:
    result = requests.get(Settings.url + '/api/list/all')
    list_output.write(result.text)

with open('autostew_back/tests/test_assets/empty_session.json', 'w') as session_output:
    result = requests.get(Settings.url + '/api/session/status?attributes=1&members=1&participants=1')
    session_output.write(result.text)