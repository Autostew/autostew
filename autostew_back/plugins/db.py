from autostew_back.gameserver.server import Server as DedicatedServer

name = 'DB'


def init(server: DedicatedServer):
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autostew.settings")
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()
