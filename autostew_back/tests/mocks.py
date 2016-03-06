
api_result_ok = """{
  "result" : "ok"
}"""


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
