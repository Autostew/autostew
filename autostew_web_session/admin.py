from django.contrib import admin
from .models.models import *


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'grid_size', 'ingame_id']
    search_fields = ['name', 'grid_size', 'ingame_id']


@admin.register(VehicleClass)
class VehicleClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'ingame_id']
    search_fields = ['name', 'ingame_id']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_filter = ['vehicle_class']
    list_display = ['name', 'ingame_id', 'vehicle_class']
    search_fields = ['name', 'ingame_id', 'vehicle_class']


@admin.register(Livery)
class LiveryAdmin(admin.ModelAdmin):
    list_filter = ['vehicle']
    list_display = ['name', 'id_for_vehicle', 'vehicle']
    search_fields = ['name', 'id_for_vehicle', 'vehicle']


@admin.register(SessionSetup)
class SessionSetupAdmin(admin.ModelAdmin):
    list_filter = [
        'is_template',
        'server_controls_setup',
        'server_controls_track',
        'server_controls_vehicle_class',
        'server_controls_vehicle',
        'public',
    ]
    list_display = [
        'name',
        'is_template',
        'public',
        'track',
        'vehicle_class'
    ]
    search_fields = [
        'name',
        'track__name',
        'vehicle_class__name',
        'vehicle__name'
    ]


@admin.register(SetupRotationEntry)
class SetupRotationEntryAdmin(admin.ModelAdmin):
    list_filter = ['server', 'setup']
    list_display = ['order', 'server', 'setup']


@admin.register(SetupQueueEntry)
class SetupQueueEntryAdmin(admin.ModelAdmin):
    list_filter = ['server', 'setup']
    list_display = ['order', 'server', 'setup']


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_filter = ['running']
    list_display = ['name', 'running', 'last_ping', 'average_player_latency', 'current_session']
    search_fields = ['name', 'current_session__setup_actual__track__name']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_filter = ['server', 'planned', 'running', 'finished', 'setup_actual__public']
    list_display = ['id', 'server', 'setup_template', 'start_timestamp', 'planned', 'running', 'finished']
    search_fields = ['server__name', 'setup_actual__track__name', 'lobby_id']


admin.site.register(SessionSnapshot)
admin.site.register(Member)
admin.site.register(MemberSnapshot)
admin.site.register(Participant)
admin.site.register(ParticipantSnapshot)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = ['definition']
    list_display = ['id', 'session', 'definition', 'timestamp', 'raw']
    search_fields = ['raw']

admin.site.register(RaceLapSnapshot)
admin.site.register(Lap)
admin.site.register(Sector)
