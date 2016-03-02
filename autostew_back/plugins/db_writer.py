import json

from autostew_back.gameserver.lists import ListName
from autostew_web_session.models import Server, Track, EventDefinition, SessionFlagDefinition, DamageDefinition, WeatherDefinition, PlayerFlagDefinition, AllowedViewsDefinition, FuelUsageDefinition, \
    GameModeDefinition, VehicleClass, PenaltyDefinition, Vehicle, Livery, SessionAttributeDefinition, MemberAttributeDefinition, ParticipantAttributeDefinition, \
    TireWearDefinition

name = 'DB writer'
enum_tables = [Server, Track, EventDefinition, SessionFlagDefinition, DamageDefinition, WeatherDefinition, PlayerFlagDefinition, AllowedViewsDefinition, FuelUsageDefinition,
               GameModeDefinition, VehicleClass, PenaltyDefinition, Vehicle, Livery]


def init(server):
    # _recreate_enums(server) # TODO set with parameter
    try:
        server_in_db = Server.objects.get(name=server.settings.server_name)
    except Server.DoesNotExist:
        server_in_db = Server(name=server.settings.server_name, running=True)
    server_in_db.running = True
    server_in_db.save()


def tick(server):
    pass


def event(server, event):
    pass


def _recreate_enums(server):
    _clear_enums()
    _create_enums(server)


def _clear_enums():
    for e in enum_tables:
        e.objects.all().delete()


def _create_enums(server):
    def _create_name_value(model, listname):
        for i in server.lists[listname].list:
            model(name=i.name, id=i.value).save(True)

    def _create_attribute(model, listname):
        for i in server.lists[listname].list:
            model(name=i.name, type=i.type, access=i.access, description=i.description).save(True)

    _create_name_value(VehicleClass, ListName.vehicle_classes)
    _create_name_value(GameModeDefinition, ListName.game_modes)
    _create_name_value(TireWearDefinition, ListName.game_modes)
    _create_name_value(PenaltyDefinition, ListName.penalties)
    _create_name_value(FuelUsageDefinition, ListName.fuel_usages)
    _create_name_value(AllowedViewsDefinition, ListName.allowed_views)
    _create_name_value(WeatherDefinition, ListName.weathers)
    _create_name_value(DamageDefinition, ListName.damage)
    _create_name_value(SessionFlagDefinition, ListName.session_flags)

    _create_attribute(SessionAttributeDefinition, ListName.session_attributes)
    _create_attribute(MemberAttributeDefinition, ListName.member_attributes)
    _create_attribute(ParticipantAttributeDefinition, ListName.participant_attributes)

    for pflag in server.lists[ListName.player_flags].list:
        if pflag.value == 0:
            continue
        PlayerFlagDefinition(name=pflag.name, id=pflag.value).save(True)

    for track in server.lists[ListName.tracks].list:
        Track(id=track.id, name=track.name, grid_size=track.gridsize).save(True)

    for event in server.lists[ListName.events].list:
        EventDefinition(name=event.name, type=event.type, description=event.type, attributes=json.dumps(event.attributes)).save(True)

    for vehicle in server.lists[ListName.vehicles].list:
        Vehicle(id=vehicle.id, name=vehicle.name, vehicle_class=VehicleClass.objects.get(name=vehicle.class_name)).save(True)

    for livery_vehicle in server.lists[ListName.liveries].list:
        for livery in livery_vehicle.liveries:
            Livery(name=livery['name'], id_for_vehicle=livery['id'], vehicle_id=livery_vehicle.id).save(True)
