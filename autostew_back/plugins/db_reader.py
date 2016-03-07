from autostew_back.plugins import db
from autostew_web_session.models import Server

name = 'DB reader'
dependencies = [db]

server_in_db = None


def init(server):
    global server_in_db
    try:
        server_in_db = Server.objects.get(name=server.settings.server_name)
    except Server.DoesNotExist:
        server_in_db = Server(name=server.settings.server_name, running=True)
    # TODO load plugins from server
    # and then raise BreakPluginLoadingException


def load_settings():
    return server_in_db.session_setups.all()


def tick(server):
    pass


def event(server, event):
    pass
