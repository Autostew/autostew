import json
import logging

from django.core.wsgi import get_wsgi_application
from django.db import transaction

from autostew_back.gameserver.event import EventType, LeavingReason
from autostew_back.gameserver.lists import ListName
from autostew_back.gameserver.member import MemberLoadState, MemberState
from autostew_back.gameserver.participant import ParticipantState
from autostew_back.gameserver.session import SessionState, SessionStage, SessionPhase
from autostew_back.plugins import db
from autostew_web_enums import models
from autostew_web_session.models.models import Server, Track, VehicleClass, Vehicle, Livery
from autostew_web_enums.models import EventDefinition, GameModeDefinition, TireWearDefinition, PenaltyDefinition, \
    FuelUsageDefinition, AllowedViewsDefinition, PlayerFlagDefinition, WeatherDefinition, DamageDefinition, \
    SessionFlagDefinition, SessionAttributeDefinition, MemberAttributeDefinition, ParticipantAttributeDefinition


name = 'DB enum writer'

get_wsgi_application()

enum_tables = [Track, EventDefinition, SessionFlagDefinition, DamageDefinition, WeatherDefinition,
               PlayerFlagDefinition, AllowedViewsDefinition, FuelUsageDefinition,
               GameModeDefinition, VehicleClass, PenaltyDefinition, Vehicle, Livery, TireWearDefinition,
               ParticipantAttributeDefinition, MemberAttributeDefinition, SessionAttributeDefinition]

true_enums = [
    (EventType, models.EventType),
    (LeavingReason, models.LeavingReason),
    (MemberLoadState, models.MemberLoadState),
    (MemberState, models.MemberState),
    (ParticipantState, models.ParticipantState),
    (SessionState, models.SessionState),
    (SessionStage, models.SessionStage),
    (SessionPhase, models.SessionPhase),
]


def env_init(server):
    _recreate_enums(server)


@transaction.atomic
def _recreate_enums(server):
    _clear_enums()
    _create_enums(server)


def _clear_enums():
    for e in enum_tables:
        e.objects.all().delete()
    for enum, model in true_enums:
        model.objects.all().delete()


def _create_enums(server):
    def _create_name_value(model, listname):
        logging.info("Creating enum {}".format(listname))
        for i in server.lists[listname].list:
            model(name=i.name, ingame_id=i.value).save(True)

    def _create_attribute(model, listname):
        logging.info("Creating attribute {}".format(listname))
        for i in server.lists[listname].list:
            model(name=i.name, type=i.type, access=i.access, description=i.description).save(True)

    def _create_true_enum(enum, orm):
        for i in enum:
            orm(name=i.value).save(True)

    for enum, orm in true_enums:
        _create_true_enum(enum, orm)

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
    logging.info("{} tracks".format(len(server.lists[ListName.tracks].list)))

    logging.info("Creating Events")
    for event in server.lists[ListName.events].list:
        EventDefinition(name=event.name, type=event.type, description=event.type, attributes=json.dumps(event.attributes)).save(True)

    logging.info("Creating Vehicles")
    for i, vehicle in enumerate(server.lists[ListName.vehicles].list):
        if i % 10 == 0 and i > 0:
            logging.info("Created {} out of {} vehicles".format(i, len(server.lists[ListName.vehicles].list)))
        vehicle_in_db = Vehicle(
            ingame_id=vehicle.id,
            name=vehicle.name,
            vehicle_class=VehicleClass.objects.get(name=vehicle.vehicle_class.name)
        )
        vehicle_in_db.save(True)
        for livery in vehicle.liveries.list:
            Livery(
                name=livery.name,
                id_for_vehicle=livery.id,
                vehicle=vehicle_in_db
            ).save(True)
