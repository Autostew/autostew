from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.aggregates import Min

from autostew_web_enums import models as enum_models


class Track(models.Model):
    class Meta:
        ordering = ['name']

    ingame_id = models.IntegerField(help_text='pCars internal ID')
    name = models.CharField(max_length=100)
    grid_size = models.SmallIntegerField()
    track_latitude = models.IntegerField(default=0)
    track_longitude = models.IntegerField(default=0)
    track_altitude = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown', 'grid_size': 0})[0]

    def get_absolute_url(self):
        return reverse('session:track', args=[str(self.id)])

    def get_fastest_laps_by_vehicle(self, vehicle):
        return Lap.objects.filter(
            session__setup_actual__track=self,
            participant__vehicle=vehicle,
            count_this_lap=True,
            participant__is_player=True,
        ).values(
            'participant',
            'participant__member__steam_user__display_name',
            'participant__vehicle__name'
        ).annotate(fastest_lap_time=Min('lap_time')).order_by('fastest_lap_time')

    def get_fastest_laps_by_vehicle_class(self, vehicle_class):
        return Lap.objects.filter(
            session__setup_actual__track=self,
            participant__vehicle__vehicle_class=vehicle_class,
            count_this_lap=True,
            participant__is_player=True,
        ).values(
            'participant__name',
            'participant__vehicle__name'
        ).annotate(fastest_lap_time=Min('lap_time')).order_by('fastest_lap_time')


class VehicleClass(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class Vehicle(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50)
    ingame_id = models.IntegerField(help_text='pCars internal ID')
    vehicle_class = models.ForeignKey(VehicleClass, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_default(cls, ingame_id):
        return cls.objects.get_or_create(ingame_id=ingame_id, defaults={'name': 'Unknown'})[0]


class Livery(models.Model):
    class Meta:
        ordering = ['vehicle__name', 'name']
        verbose_name_plural = "Liveries"

    name = models.CharField(max_length=50)
    id_for_vehicle = models.IntegerField(help_text='pCars internal ID')
    vehicle = models.ForeignKey(Vehicle, null=True)

    @classmethod
    def get_or_create_default(cls, id_for_vehicle, vehicle):
        return cls.objects.get_or_create(
            id_for_vehicle=id_for_vehicle,
            vehicle=vehicle,
            defaults={'name': 'Unknown'}
        )[0]

    def __str__(self):
        return "{} for {}".format(self.name, self.vehicle.name)


class SetupRotationEntry(models.Model):
    class Meta:
        ordering = ('server', 'order', )
        verbose_name_plural = "Rotated setups"
    order = models.IntegerField(help_text='Index of setup in order')
    setup = models.ForeignKey('SessionSetup', on_delete=models.CASCADE, limit_choices_to={'is_template': True})
    server = models.ForeignKey('Server', on_delete=models.CASCADE)


class SetupQueueEntry(models.Model):
    class Meta:
        ordering = ('server', 'order', )
        verbose_name_plural = "Queued setups"
    order = models.IntegerField(help_text='Index of setup in order')
    setup = models.ForeignKey('SessionSetup', on_delete=models.CASCADE, limit_choices_to={'is_template': True})
    server = models.ForeignKey('Server', on_delete=models.CASCADE)


class RaceLapSnapshot(models.Model):
    class Meta:
        ordering = ['session_id', 'lap']

    session = models.ForeignKey('Session')
    snapshot = models.OneToOneField('Session', related_name='+')
    lap = models.IntegerField()

    def get_absolute_url(self):
        return self.snapshot.get_absolute_url()


class Lap(models.Model):
    class Meta:
        ordering = ['session_id', 'lap']

    session = models.ForeignKey('Session', related_name='lap_set')
    session_stage = models.ForeignKey(enum_models.SessionStage)
    participant = models.ForeignKey('Participant')
    lap = models.IntegerField()
    count_this_lap = models.BooleanField()
    lap_time = models.IntegerField()
    position = models.IntegerField()
    sector1_time = models.IntegerField()
    sector2_time = models.IntegerField()
    sector3_time = models.IntegerField()
    distance_travelled = models.IntegerField()

    def is_personal_sector1_race_best_in_stage(self):
        return self._best_in_stage_evaluation('sector1_time')

    def is_personal_sector2_race_best_in_stage(self):
        return self._best_in_stage_evaluation('sector2_time')

    def is_personal_sector3_race_best_in_stage(self):
        return self._best_in_stage_evaluation('sector3_time')

    def is_personal_race_best_in_stage(self):
        return self._best_in_stage_evaluation('lap_time')

    def _best_in_stage_evaluation(self, field_name):
        return getattr(self, field_name) <= self.participant.lap_set.filter(
            **{
                '{}__gt'.format(field_name): 0,
                'session_stage': self.session_stage
            }
        ).aggregate(Min(field_name))['{}__min'.format(field_name)]


class Sector(models.Model):
    class Meta:
        ordering = ['session_id', 'lap', 'sector']

    session = models.ForeignKey('Session')
    session_stage = models.ForeignKey(enum_models.SessionStage)
    participant = models.ForeignKey('Participant')
    lap = models.IntegerField()
    count_this_lap = models.BooleanField()
    sector = models.SmallIntegerField()
    sector_time = models.IntegerField()
