from django.contrib import admin
from .models import *

admin.site.register(Server)
admin.site.register(Track)
admin.site.register(EventDefinition)
admin.site.register(GameModeDefinition)
admin.site.register(TireWearDefinition)
admin.site.register(PenaltyDefinition)
admin.site.register(FuelUsageDefinition)
admin.site.register(AllowedViewsDefinition)
admin.site.register(PlayerFlagDefinition)
admin.site.register(WeatherDefinition)
admin.site.register(DamageDefinition)
admin.site.register(SessionFlagDefinition)
admin.site.register(VehicleClass)
admin.site.register(Vehicle)
admin.site.register(Livery)
admin.site.register(SessionAttributeDefinition)
admin.site.register(MemberAttributeDefinition)
admin.site.register(ParticipantAttributeDefinition)

