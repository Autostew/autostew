
api_result_ok = """{
  "result" : "ok"
}"""


class MockedSettings():
    def __init__(self):
        self.url = None


class MockedRequestsResult():
    def __init__(self, text, ok):
        self.ok = ok
        self.text = text


class MockedServer():
    def __init__(self):
        self.settings = MockedSettings()