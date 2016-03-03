from django.contrib import admin
from .models import *

admin.site.register(Server)
admin.site.register(Track)
admin.site.register(VehicleClass)
admin.site.register(Vehicle)
admin.site.register(Livery)
admin.site.register(SessionSetup)
admin.site.register(Session)
admin.site.register(SessionSnapshot)
admin.site.register(Member)
admin.site.register(MemberSnapshot)
admin.site.register(Participant)
admin.site.register(ParticipantSnapshot)
admin.site.register(Event)
admin.site.register(RaceLapSnapshot)
admin.site.register(Lap)
admin.site.register(Sector)
