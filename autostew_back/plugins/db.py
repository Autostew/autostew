from autostew_back.gameserver.server import Server as DedicatedServer

name = 'DB'


def init(server: DedicatedServer):
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()

# this is needed, else other plugins won't load
init(None)
