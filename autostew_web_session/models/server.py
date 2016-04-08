import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from autostew_web_session.models import models as session_models


class Server(models.Model):
    class Meta:
        ordering = ('name', )

    name = models.CharField(max_length=50, unique=True,
                            help_text='To successfully rename a server you will need to change it\'s settings too')

    setup_rotation_index = models.IntegerField()
    setup_rotation = models.ManyToManyField('SessionSetup',
                                            related_name='rotated_in_server', through='SetupRotationEntry',
                                            help_text="Setups that will be used on this server's rotation")

    setup_queue = models.ManyToManyField('SessionSetup',
                                         related_name='queued_in_server', through='SetupQueueEntry',
                                         blank=True,
                                         help_text="If set, this will be the next setup used")

    scheduled_sessions = models.ManyToManyField('Session', limit_choices_to={'planned': True},
                                                related_name='schedule_at_servers',
                                                blank=True,
                                                help_text="These schedule setups will be used (on their scheduled time)")

    running = models.BooleanField(help_text="This value should not be changed manually")
    current_session = models.ForeignKey('Session', null=True, related_name='+', blank=True)
    last_ping = models.DateTimeField(null=True, blank=True,
                                     help_text="Last time the server reported to be alive")
    average_player_latency = models.IntegerField(null=True, blank=True)
    # TODO joinable = models.BooleanField()
    # TODO state = server.state!!

    @property
    def is_up(self):
        return self.running and self.time_since_last_ping < 120

    @property
    def time_since_last_ping(self):
        return int((timezone.now() - self.last_ping).total_seconds())

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('session:server', args=[str(self.name)])

    def pop_next_queued_setup(self, peek=False):
        ordered_queue = session_models.SetupQueueEntry.objects.filter(server=self).order_by('order')
        if len(ordered_queue) == 0:
            return None
        next_setup = ordered_queue[0].setup
        if not peek:
            ordered_queue[0].delete()
        return next_setup

    def next_scheduled_session(self):
        for scheduled_session_it in self.scheduled_sessions.filter(running=False, finished=False):
            if (
                (not scheduled_session_it.schedule_date or scheduled_session_it.schedule_date == datetime.date.today()) and
                scheduled_session_it.schedule_time + datetime.timedelta(seconds=300) > datetime.time()
            ):
                return scheduled_session_it
        return None