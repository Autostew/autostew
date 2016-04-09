import datetime
import time

from django.utils import timezone
from django.core.wsgi import get_wsgi_application

# This line has to happen before importing models
import autostew_web_session.models.server

get_wsgi_application()

from autostew_web_session.models import models
from autostew_web_session.models.models import SetupRotationEntry

name = 'DB'
ping_interval = 10

last_ping = None


def init(server: models.Server):
    server.running = True
    server.state = server.state
    if not server.id:
        server.save()
    server.save()
    _ping(server)


def tick(server: models.Server):
    if time.time() - last_ping >= ping_interval:
        _ping(server)


def destroy(server: models.Server):
    server.current_session = None
    server.running = False
    server.save()


def _ping(server: models.Server):
    global last_ping
    server.last_ping = timezone.make_aware(datetime.datetime.now())
    if len(server.members.elements) == 0:
        server.average_player_latency = None
    else:
        server.average_player_latency = sum([member.ping.get() for member in server.members.elements]) / len(server.members.elements)
    last_ping = time.time()
    server.save()
