import logging
from os import listdir
from os.path import isfile, join

api_result_ok = """{
  "result" : "ok"
}"""

replay_api_status_format = """{{
  "result" : "ok",
  "response" : {}
}}"""

replay_api_events_format = """{{
  "result" : "ok",
  "response" : {}
}}"""


class MockedSettings:
    def __init__(self):
        self.url = 'http://localhost:9000'


class MockedRequestsResult:
    def __init__(self, text, ok):
        self.ok = ok
        self.text = text


class MockedServer:
    def __init__(self):
        self.settings = MockedSettings()


class FakeApi:
    def __init__(
            self,
            status_result='autostew_back/tests/test_assets/empty_session.json',
            events_result='autostew_back/tests/test_assets/events_empty.json'
    ):
        self.status_result = status_result
        self.events_result = events_result

    def fake_request(self, url):
        if url == "http://localhost:9000/api/list/all?":
            with open('autostew_back/tests/test_assets/lists.json') as file_input:
                return MockedRequestsResult(file_input.read(), True)
        elif url == "http://localhost:9000/api/version?":
            with open('autostew_back/tests/test_assets/version.json') as file_input:
                return MockedRequestsResult(file_input.read(), True)
        elif url == "http://localhost:9000/api/help?":
            with open('autostew_back/tests/test_assets/help.json') as file_input:
                return MockedRequestsResult(file_input.read(), True)
        elif url.startswith("http://localhost:9000/api/session/status"):
            with open(self.status_result) as file_input:
                return MockedRequestsResult(file_input.read(), True)
        elif url.startswith("http://localhost:9000/api/session/set_attributes") or \
                url.startswith("http://localhost:9000/api/session/set_next_attributes") or \
                url.startswith("http://localhost:9000/api/session/send_chat"):
            return MockedRequestsResult(api_result_ok, True)
        elif url in ("http://localhost:9000/api/log/range?count=1&offset=-1",
                     "http://localhost:9000/api/log/range?offset=-1&count=1"):
            with open('autostew_back/tests/test_assets/events_empty.json') as file_input:
                return MockedRequestsResult(file_input.read(), True)
        elif url.startswith("http://localhost:9000/api/log/range?"):
            with open(self.events_result) as file_input:
                return MockedRequestsResult(file_input.read(), True)
        else:
            raise Exception("Url not mocked: {}".format(url))


class ApiReplay(FakeApi):
    class RecordFinished(Exception):
        pass

    def __init__(self, record_path):
        FakeApi.__init__(self)
        self._record_path = record_path
        self.event_fetch_count = 0
        self.status_fetch_count = 0
        self.event_replys = {
            0: {
                'status_reply_list': []
            }
        }
        event_index = 0
        files = [f for f in listdir(record_path) if isfile(join(record_path, f)) and not f.startswith('.') and f.endswith('.json')]
        files = sorted(files, key=lambda filename: int(filename.split('-')[0]))
        for file in files:
            with open(join(record_path, file)) as filep:
                filename = file.split('.')[0]
                absolute_index, type, class_index = filename.split('-')
                if type == 'status':
                    self.event_replys[event_index]['status_reply_list'].append(filep.read())
                if type == 'events':
                    event_index += 1
                    self.event_replys[event_index] = {
                        'status_reply_list': [],
                        'event_reply': filep.read()
                    }
        logging.info("{} recorded API replies loaded".format(len(files)))

    def fake_request(self, url):
        if url in ("http://localhost:9000/api/log/range?count=1&offset=-1",
                   "http://localhost:9000/api/log/range?offset=-1&count=1"):
            return FakeApi.fake_request(self, url)
        elif url.startswith("http://localhost:9000/api/log/range?"):
            self.event_fetch_count += 1
            self.status_fetch_count = 0
            if self.event_fetch_count >= len(self.event_replys):
                raise self.RecordFinished
            return MockedRequestsResult(
                replay_api_status_format.format(self.event_replys[self.event_fetch_count]['event_reply']),
                True
            )
        elif url.startswith("http://localhost:9000/api/session/status"):
            event_idx_to_use = self.event_fetch_count
            while len(self.event_replys[event_idx_to_use]['status_reply_list']) == 0:
                event_idx_to_use -= 1
                self.status_fetch_count = len(self.event_replys[event_idx_to_use]['status_reply_list']) - 1
            if self.status_fetch_count >= len(self.event_replys[event_idx_to_use]['status_reply_list']):
                self.status_fetch_count = len(self.event_replys[event_idx_to_use]['status_reply_list']) - 1
            result = MockedRequestsResult(
                replay_api_events_format.format(self.event_replys[event_idx_to_use]['status_reply_list'][self.status_fetch_count]),
                True
            )
            self.status_fetch_count += 1
            return result
        else:
            return FakeApi.fake_request(self, url)
