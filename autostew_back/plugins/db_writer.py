import json

from autostew_back.gameserver.lists import ListName
from autostew_back.gameserver.session import SessionFlags, Privacy
from autostew_web_session.models import Server, Track, VehicleClass, Vehicle, Livery, SessionSetup
from autostew_web_enums.models import EventDefinition, GameModeDefinition, TireWearDefinition, PenaltyDefinition, \
    FuelUsageDefinition, AllowedViewsDefinition, PlayerFlagDefinition, WeatherDefinition, DamageDefinition, \
    SessionFlagDefinition, SessionAttributeDefinition, MemberAttributeDefinition, ParticipantAttributeDefinition

name = 'DB writer'
enum_tables = [Server, Track, EventDefinition, SessionFlagDefinition, DamageDefinition, WeatherDefinition, PlayerFlagDefinition, AllowedViewsDefinition, FuelUsageDefinition,
               GameModeDefinition, VehicleClass, PenaltyDefinition, Vehicle, Livery, TireWearDefinition]


def env_init(server):
    _recreate_enums(server)


def init(server):
    try:
        server_in_db = Server.objects.get(name=server.settings.server_name)
    except Server.DoesNotExist:
        server_in_db = Server(name=server.settings.server_name, running=True)
    server_in_db.running = True
    server_in_db.save()
    _create_session(server, server_in_db)  # TODO should be _find_or_create_session()


def tick(server):
    pass


def event(server, event):
    pass


def _create_session(server, server_in_db):
    flags = server.session.flags.get_flags()
    setup = SessionSetup(
        server_controls_setup=server.session.server_controls_setup.get(),
        server_controls_track=server.session.server_controls_track.get(),
        server_controls_vehicle_class=server.session.server_controls_vehicle_class.get(),
        server_controls_vehicle=server.session.server_controls_vehicle.get(),
        grid_size=server.session.grid_size.get(),
        max_players=server.session.max_players.get(),
        opponent_difficulty=server.session.opponent_difficulty.get(),
        force_identical_vehicles=SessionFlags.force_identical_vehicles in flags,
        allow_custom_vehicle_setup=SessionFlags.allow_custom_vehicle_setup in flags,
        force_realistic_driving_aids=SessionFlags.force_realistic_driving_aids in flags,
        abs_allowed=SessionFlags.abs_allowed in flags,
        sc_allowed=SessionFlags.sc_allowed in flags,
        tcs_allowed=SessionFlags.tcs_allowed in flags,
        force_manual=SessionFlags.force_manual in flags,
        rolling_starts=SessionFlags.rolling_starts in flags,
        force_same_vehicle_class=SessionFlags.force_same_vehicle_class in flags,
        fill_session_with_ai=SessionFlags.fill_session_with_ai in flags,
        mechanical_failures=SessionFlags.mechanical_failures in flags,
        auto_start_engine=SessionFlags.auto_start_engine in flags,
        timed_race=SessionFlags.timed_race in flags,
        ghost_griefers=SessionFlags.ghost_griefers in flags,
        enforced_pitstop=SessionFlags.enforced_pitstop in flags,
        practice1_length=server.session.practice1_length.get(),
        practice2_length=server.session.practice2_length.get(),
        qualify_length=server.session.qualify_length.get(),
        warmup_length=server.session.warmup_length.get(),
        race1_length=server.session.race1_length.get(),
        race2_length=server.session.race2_length.get(),
        public=server.session.privacy.get() == Privacy.public,
        friends_can_join=server.session.privacy.get() in (Privacy.public, Privacy.friends),
        damage=DamageDefinition.objects.get(id=server.session.damage.get()) if server.session.damage.get() else None,
        tire_wear=TireWearDefinition.objects.get(id=server.session.tire_wear.get()) if server.session.tire_wear.get() else None,
        fuel_usage=FuelUsageDefinition.objects.get(id=server.session.fuel_usage.get()) if server.session.fuel_usage.get() else None,
        penalties=PenaltyDefinition.objects.get(id=server.session.penalties.get()) if server.session.penalties.get() else None,
        allowed_views=AllowedViewsDefinition.objects.get(id=server.session.allowed_views.get()) if server.session.allowed_views.get() else None,
        track=Track.objects.get(id=server.session.track.get()) if server.session.track.get() else None,
        vehicle_class=VehicleClass.objects.get(id=server.session.vehicle_class.get()) if server.session.vehicle_class.get() else None,
        vehicle=Vehicle.objects.get(id=server.session.vehicle.get()) if server.session.vehicle.get() else None,
        date_year=server.session.date_year.get(),
        date_month=server.session.date_month.get(),
        date_day=server.session.date_day.get(),
        date_hour=server.session.date_hour.get(),
        date_minute=server.session.date_minute.get(),
        date_progression=server.session.date_progression.get(),
        weather_progression=server.session.weather_progression.get(),
        weather_slots=server.session.weather_slots.get(),
        weather_1=WeatherDefinition.objects.get(id=server.session.weather_1.get()) if server.session.weather_1.get() else None,
        weather_2=WeatherDefinition.objects.get(id=server.session.weather_2.get()) if server.session.weather_2.get() else None,
        weather_3=WeatherDefinition.objects.get(id=server.session.weather_3.get()) if server.session.weather_3.get() else None,
        weather_4=WeatherDefinition.objects.get(id=server.session.weather_4.get()) if server.session.weather_4.get() else None,
        game_mode=GameModeDefinition.objects.get(id=server.session.game_mode.get()) if server.session.game_mode.get() else None,
        track_latitude=server.session.track_latitude.get(),
        track_longitude=server.session.track_longitude.get(),
        track_altitude=server.session.track_altitude.get(),
    ).save(True)


def _make_snapshot(server):
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
