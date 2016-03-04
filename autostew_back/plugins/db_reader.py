from autostew_back.plugins import db

name = 'DB reader'
dependencies = [db]


def init(server):
    # TODO load plugins from server
    # and then raise BreakPluginLoadingException
    pass


def tick(server):
    pass


def event(server, event):
    pass
