import json
import logging

from autostew_back.gameserver.event import EventType
from autostew_back.gameserver.lists import ListName
from autostew_back.gameserver.member import MemberFlags
from autostew_back.gameserver.session import SessionFlags, Privacy
from autostew_back.plugins import db
from autostew_web_session.models import Server, Track, VehicleClass, Vehicle, Livery, SessionSetup, Session, \
    SessionSnapshot, Member, Participant, MemberSnapshot, ParticipantSnapshot
from autostew_web_enums.models import EventDefinition, GameModeDefinition, TireWearDefinition, PenaltyDefinition, \
    FuelUsageDefinition, AllowedViewsDefinition, PlayerFlagDefinition, WeatherDefinition, DamageDefinition, \
    SessionFlagDefinition, SessionAttributeDefinition, MemberAttributeDefinition, ParticipantAttributeDefinition


name = 'DB writer'
dependencies = [db]

enum_tables = [Track, EventDefinition, SessionFlagDefinition, DamageDefinition, WeatherDefinition,
               PlayerFlagDefinition, AllowedViewsDefinition, FuelUsageDefinition,
               GameModeDefinition, VehicleClass, PenaltyDefinition, Vehicle, Livery, TireWearDefinition]


def env_init(server):
    _recreate_enums(server)


def _recreate_enums(server):
    _clear_enums()
    _create_enums(server)


def _clear_enums():
    for e in enum_tables:
        e.objects.all().delete()


def _create_enums(server):
    def _create_name_value(model, listname):
        logging.info("Creating enum {}".format(listname))
        for i in server.lists[listname].list:
            model(name=i.name, ingame_id=i.value).save(True)

    def _create_attribute(model, listname):
        logging.info("Creating attribute {}".format(listname))
        for i in server.lists[listname].list:
            model(name=i.name, type=i.type, access=i.access, description=i.description).save(True)

    _create_name_value(VehicleClass, ListName.vehicle_classes)
    _create_name_value(GameModeDefinition, ListName.game_modes)
    _create_name_value(TireWearDefinition, ListName.tire_wears)
    _create_name_value(PenaltyDefinition, ListName.penalties)
    _create_name_value(FuelUsageDefinition, ListName.fuel_usages)
    _create_name_value(AllowedViewsDefinition, ListName.allowed_views)
    _create_name_value(WeatherDefinition, ListName.weathers)
    _create_name_value(DamageDefinition, ListName.damage)
    _create_name_value(SessionFlagDefinition, ListName.session_flags)

    _create_attribute(SessionAttributeDefinition, ListName.session_attributes)
    _create_attribute(MemberAttributeDefinition, ListName.member_attributes)
    _create_attribute(ParticipantAttributeDefinition, ListName.participant_attributes)

    logging.info("Creating PlayerFlags")
    for pflag in server.lists[ListName.player_flags].list:
        if pflag.value == 0:
            continue
        PlayerFlagDefinition(name=pflag.name, ingame_id=pflag.value).save(True)

    logging.info("Creating Tracks")
    for track in server.lists[ListName.tracks].list:
        Track(ingame_id=track.id, name=track.name, grid_size=track.gridsize).save(True)

    logging.info("Creating Events")
    for event in server.lists[ListName.events].list:
        EventDefinition(name=event.name, type=event.type, description=event.type, attributes=json.dumps(event.attributes)).save(True)

    logging.info("Creating Vehicles")
    for vehicle in server.lists[ListName.vehicles].list:
        Vehicle(ingame_id=vehicle.id, name=vehicle.name, vehicle_class=VehicleClass.objects.get(name=vehicle.class_name)).save(True)

    logging.info("Creating Liveries")
    for livery_vehicle in server.lists[ListName.liveries].list:
        for livery in livery_vehicle.liveries:
            Livery(name=livery['name'], id_for_vehicle=livery['id'], vehicle=Vehicle.objects.get(ingame_id=livery_vehicle.id)).save(True)
