from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Min

from autostew_web_enums import models as enum_models
from autostew_web_session.models.session import Session


class Participant(models.Model):
    class Meta:
        ordering = ['name']

    member = models.ForeignKey('Member', null=True, blank=True)  # AI will be NULL
    session = models.ForeignKey(Session)
    still_connected = models.BooleanField()

    ingame_id = models.IntegerField()
    refid = models.IntegerField()
    name = models.CharField(max_length=200)
    is_ai = models.BooleanField()
    vehicle = models.ForeignKey('Vehicle', null=True, blank=True)  # NULL because AI owner change will do that
    livery = models.ForeignKey('Livery', null=True, blank=True)  # NULL because AI owner change will do that

    def get_absolute_url(self):
        return reverse('session:participant', args=[str(self.session.id), str(self.ingame_id)])


class ParticipantSnapshot(models.Model):
    class Meta:
        ordering = ['race_position']

    snapshot = models.ForeignKey('SessionSnapshot')
    participant = models.ForeignKey('Participant')
    still_connected = models.BooleanField()

    grid_position = models.IntegerField()
    race_position = models.IntegerField()
    current_lap = models.IntegerField()
    current_sector = models.IntegerField()
    sector1_time = models.IntegerField()
    sector2_time = models.IntegerField()
    sector3_time = models.IntegerField()
    last_lap_time = models.IntegerField()
    fastest_lap_time = models.IntegerField()
    state = models.ForeignKey(enum_models.ParticipantState)
    headlights = models.BooleanField()
    wipers = models.BooleanField()
    speed = models.IntegerField()
    gear = models.SmallIntegerField()
    rpm = models.IntegerField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    position_z = models.IntegerField()
    orientation = models.IntegerField()
    total_time = models.IntegerField()

    def get_member_snapshot(self):
        return self.snapshot.member_snapshots.get(member=self.participant.member)

    def last_lap_is_fastest_in_shapshot(self):
        try:
            return self.last_lap_time <= self.snapshot.participantsnapshot_set.filter(last_lap_time__gt=0).aggregate(Min('last_lap_time'))['last_lap_time__min']
        except TypeError:
            return False

    def last_lap_is_fastest_in_race(self):
        try:
            return self.last_lap_time <= self.snapshot.participantsnapshot_set.filter(fastest_lap_time__gt=0).aggregate(Min('fastest_lap_time'))['fastest_lap_time__min']
        except TypeError:
            return False

    def fastest_lap_is_fastest_in_race(self):
        try:
            return self.fastest_lap_time <= self.snapshot.participantsnapshot_set.filter(fastest_lap_time__gt=0).aggregate(Min('fastest_lap_time'))['fastest_lap_time__min']
        except TypeError:
            return False

    def gap(self):
        if self.race_position == 1:
            return None
        if self.snapshot.session_stage.name.startswith("Race"):
            if not self.total_time:
                return None
            return self.total_time - ParticipantSnapshot.objects.get(snapshot=self.snapshot, race_position=1).total_time
        else:
            if not self.fastest_lap_time:
                return None
            return self.fastest_lap_time - ParticipantSnapshot.objects.get(snapshot=self.snapshot, race_position=1).fastest_lap_time