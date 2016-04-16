from django.db import models

from autostew_web_enums.models import LeavingReason


class Member(models.Model):
    class Meta:
        ordering = ['name']

    parent = models.ForeignKey('self', null=True, blank=True)
    steam_user = models.ForeignKey('autostew_web_users.SteamUser')
    session = models.ForeignKey('Session')
    still_connected = models.BooleanField()

    ingame_load_state = models.ForeignKey('autostew_web_enums.MemberLoadState')
    ping = models.IntegerField()
    ingame_index = models.IntegerField()
    ingame_state = models.ForeignKey('autostew_web_enums.MemberState')
    join_time = models.IntegerField()
    is_host = models.BooleanField()
    leaving_reason = models.ForeignKey(LeavingReason, null=True, blank=True)

    vehicle = models.ForeignKey('Vehicle')
    livery = models.ForeignKey('Livery')
    refid = models.IntegerField()
    steam_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    setup_used = models.BooleanField()
    controller_gamepad = models.BooleanField()
    controller_wheel = models.BooleanField()
    aid_steering = models.BooleanField()
    aid_braking = models.BooleanField()
    aid_abs = models.BooleanField()
    aid_traction = models.BooleanField()
    aid_stability = models.BooleanField()
    aid_no_damage = models.BooleanField()
    aid_auto_gears = models.BooleanField()
    aid_auto_clutch = models.BooleanField()
    model_normal = models.BooleanField()
    model_experienced = models.BooleanField()
    model_pro = models.BooleanField()
    model_elite = models.BooleanField()
    aid_driving_line = models.BooleanField()
    valid = models.BooleanField()

    def create_snapshot(self, session_snapshot):
        snapshot = Member.objects.get(pk=self.pk)
        snapshot.pk = None
        snapshot.parent = self
        snapshot.save()
        return snapshot
