from django.db import models

from autostew_web_enums import models as enum_models


class Member(models.Model):
    class Meta:
        ordering = ['name']

    steam_user = models.ForeignKey('autostew_web_users.SteamUser')
    session = models.ForeignKey('Session')
    still_connected = models.BooleanField()

    vehicle = models.ForeignKey('Vehicle')
    livery = models.ForeignKey('Livery')
    refid = models.IntegerField()
    steam_id = models.CharField(max_length=200)  # TODO duplicate in SteamUser
    name = models.CharField(max_length=200)

    setup_used = models.BooleanField()
    controller_gamepad = models.BooleanField()  # TODO these 2 are ugly
    controller_wheel = models.BooleanField()
    aid_steering = models.BooleanField()
    aid_braking = models.BooleanField()
    aid_abs = models.BooleanField()
    aid_traction = models.BooleanField()
    aid_stability = models.BooleanField()
    aid_no_damage = models.BooleanField()
    aid_auto_gears = models.BooleanField()
    aid_auto_clutch = models.BooleanField()
    model_normal = models.BooleanField()  # TODO these 4 are ugly
    model_experienced = models.BooleanField()
    model_pro = models.BooleanField()
    model_elite = models.BooleanField()
    aid_driving_line = models.BooleanField()
    valid = models.BooleanField()  # idk what this means

    def finishing_position(self):
        race_stage = self.session.get_race_stage()
        if race_stage is None or race_stage.result_snapshot is None:
            return None
        try:
            return race_stage.result_snapshot.member_snapshots.get(member=self).get_participant_snapshot().race_position
        except MemberSnapshot.DoesNotExist:
            return None


class MemberSnapshot(models.Model):
    class Meta:
        ordering = ['member__name']

    member = models.ForeignKey(Member)
    snapshot = models.ForeignKey('SessionSnapshot', related_name='member_snapshots')
    still_connected = models.BooleanField()
    load_state = models.ForeignKey(enum_models.MemberLoadState)
    ping = models.IntegerField()
    index = models.IntegerField()
    state = models.ForeignKey(enum_models.MemberState)
    join_time = models.IntegerField()
    host = models.BooleanField()

    def get_participant_snapshot(self):
        return self.snapshot.participantsnapshot_set.get(participant__member=self.member)