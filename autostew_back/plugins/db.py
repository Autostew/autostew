import datetime
import time

from django.utils import timezone
from django.core.wsgi import get_wsgi_application

# This line has to happen before importing models

get_wsgi_application()

from autostew_back.gameserver.server import Server as DedicatedServer
from autostew_web_session import models
from autostew_web_session.models import SetupRotationEntry

name = 'DB'
ping_interval = 10

server_in_db = None
last_ping = None


def init(server: DedicatedServer):
    global server_in_db
    try:
        server_in_db = models.Server.objects.get(name=server.settings.server_name)
    except models.Server.DoesNotExist:
        server_in_db = models.Server(name=server.settings.server_name, running=True)
    server_in_db.running = True
    server_in_db.state = server.state
    if not server_in_db.id:
        server_in_db.save()
        for i, template_setup in enumerate(models.SessionSetup.objects.filter(is_template=True)):
            SetupRotationEntry(order=i, server=server_in_db, setup=template_setup).save()
    server_in_db.save()
    _ping(server)


def tick(server: DedicatedServer):
    if time.time() - last_ping >= ping_interval:
        _ping(server)


def destroy(server: DedicatedServer):
    global server_in_db
    server_in_db.current_session = None
    server_in_db.running = False
    server_in_db.save()


def _ping(server: DedicatedServer):
    global last_ping
    server_in_db.last_ping = timezone.make_aware(datetime.datetime.now())
    if len(server.members.elements) == 0:
        server_in_db.average_player_latency = None
    else:
        server_in_db.average_player_latency = sum([member.ping.get() for member in server.members.elements]) / len(server.members.elements)
    last_ping = time.time()
    server_in_db.save()
