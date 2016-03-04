import json
import logging

from autostew_back.gameserver.event import EventType
from autostew_back.gameserver.lists import ListName
from autostew_back.gameserver.member import MemberFlags
from autostew_back.gameserver.session import SessionFlags, Privacy
from autostew_web_session.models import Server, Track, VehicleClass, Vehicle, Livery, SessionSetup, Session, \
    SessionSnapshot, Member, Participant, MemberSnapshot, ParticipantSnapshot
from autostew_web_enums.models import EventDefinition, GameModeDefinition, TireWearDefinition, PenaltyDefinition, \
    FuelUsageDefinition, AllowedViewsDefinition, PlayerFlagDefinition, WeatherDefinition, DamageDefinition, \
    SessionFlagDefinition, SessionAttributeDefinition, MemberAttributeDefinition, ParticipantAttributeDefinition

name = 'DB writer'
enum_tables = [Track, EventDefinition, SessionFlagDefinition, DamageDefinition, WeatherDefinition,
               PlayerFlagDefinition, AllowedViewsDefinition, FuelUsageDefinition,
               GameModeDefinition, VehicleClass, PenaltyDefinition, Vehicle, Livery, TireWearDefinition]
current_session = None
server_in_db = None


def env_init(server):
    _recreate_enums(server)


def init(server):
    global current_session
    global server_in_db
    try:
        server_in_db = Server.objects.get(name=server.settings.server_name)
    except Server.DoesNotExist:
        server_in_db = Server(name=server.settings.server_name, running=True)
    server_in_db.running = True
    server_in_db.state = server.state
    server_in_db.save()
    current_session = _create_session(server, server_in_db)  # TODO should be _find_or_create_session()


def tick(server):
    pass


def event(server, event):  # TODO fill out the gaps
    if event.type == EventType.lap and event.race_position == 1:
        _make_snapshot(server, current_session)
    if event.type == EventType.participant_created:
        _create_participant(current_session, event.participant)
    if event.type == EventType.participant_destroyed:
        pass
    if event.type == EventType.authenticated:
        _create_member()
    if event.type == EventType.player_left:
        pass
    if event.type == EventType.session_created:
        _create_session(server, server_in_db)
    if event.type == EventType.session_destroyed:
        pass
    if event.type == EventType.state_changed:
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
        damage=DamageDefinition.objects.get(ingame_id=server.session.damage.get()) if server.session.damage.get() else None,
        tire_wear=TireWearDefinition.objects.get(ingame_id=server.session.tire_wear.get()) if server.session.tire_wear.get() else None,
        fuel_usage=FuelUsageDefinition.objects.get(ingame_id=server.session.fuel_usage.get()) if server.session.fuel_usage.get() else None,
        penalties=PenaltyDefinition.objects.get(ingame_id=server.session.penalties.get()) if server.session.penalties.get() else None,
        allowed_views=AllowedViewsDefinition.objects.get(ingame_id=server.session.allowed_views.get()) if server.session.allowed_views.get() else None,
        track=Track.objects.get(ingame_id=server.session.track.get()) if server.session.track.get() else None,
        vehicle_class=VehicleClass.objects.get(ingame_id=server.session.vehicle_class.get()) if server.session.vehicle_class.get() else None,
        vehicle=Vehicle.objects.get(ingame_id=server.session.vehicle.get()) if server.session.vehicle.get() else None,
        date_year=server.session.date_year.get(),
        date_month=server.session.date_month.get(),
        date_day=server.session.date_day.get(),
        date_hour=server.session.date_hour.get(),
        date_minute=server.session.date_minute.get(),
        date_progression=server.session.date_progression.get(),
        weather_progression=server.session.weather_progression.get(),
        weather_slots=server.session.weather_slots.get(),
        weather_1=WeatherDefinition.objects.get(ingame_id=server.session.weather_1.get()) if server.session.weather_1.get() else None,
        weather_2=WeatherDefinition.objects.get(ingame_id=server.session.weather_2.get()) if server.session.weather_2.get() else None,
        weather_3=WeatherDefinition.objects.get(ingame_id=server.session.weather_3.get()) if server.session.weather_3.get() else None,
        weather_4=WeatherDefinition.objects.get(ingame_id=server.session.weather_4.get()) if server.session.weather_4.get() else None,
        game_mode=GameModeDefinition.objects.get(ingame_id=server.session.game_mode.get()) if server.session.game_mode.get() else None,
        track_latitude=server.session.track_latitude.get(),
        track_longitude=server.session.track_longitude.get(),
        track_altitude=server.session.track_altitude.get(),
    )
    setup.save(True)

    session = Session(
        server=server_in_db,
        setup=setup,
        lobby_id=server.lobby_id,
        max_member_count=server.max_member_count,
        planned=False,
        running=True,
        finished=False,
    )
    session.save(True)

    for member in server.members.elements:
        _create_member(session, member)

    for participant in server.participants.elements:
        _create_participant(session, participant)

    snapshot = _make_snapshot(server, session)
    session.first_snapshot = snapshot
    session.save()
    return session


def _create_member(session, member):
    member_flags = member.race_stat_flags.get_flags()
    vehicle = Vehicle.objects.get(ingame_id=member.vehicle.get()) if member.vehicle.get() else None
    member = Member(
        session=session,
        vehicle=vehicle,
        livery=Livery.objects.get(id_for_vehicle=member.livery.get(), vehicle=vehicle) if vehicle else None,
        refid=member.refid.get(),
        steam_id=member.steam_id.get(),
        name=member.name.get(),
        setup_used=MemberFlags.setup_used in member_flags,
        controller_gamepad=MemberFlags.controller_gamepad in member_flags,
        controller_wheel=MemberFlags.controller_wheel in member_flags,
        aid_steering=MemberFlags.aid_steering in member_flags,
        aid_braking=MemberFlags.aid_braking in member_flags,
        aid_abs=MemberFlags.aid_abs in member_flags,
        aid_traction=MemberFlags.aid_traction in member_flags,
        aid_stability=MemberFlags.aid_stability in member_flags,
        aid_no_damage=MemberFlags.aid_no_damage in member_flags,
        aid_auto_gears=MemberFlags.aid_auto_gears in member_flags,
        aid_auto_clutch=MemberFlags.aid_auto_clutch in member_flags,
        model_normal=MemberFlags.model_normal in member_flags,
        model_experienced=MemberFlags.model_experienced in member_flags,
        model_pro=MemberFlags.model_pro in member_flags,
        model_elite=MemberFlags.model_elite in member_flags,
        aid_driving_line=MemberFlags.aid_driving_line in member_flags,
        valid=MemberFlags.valid in member_flags,
    )
    member.save(True)
    return member


def _create_participant(session, participant):
    vehicle = Vehicle.objects.get(ingame_id=participant.vehicle.get()) if participant.vehicle.get() else None
    participant = Participant(
        member=Member.objects.get(refid=participant.refid.get(), session=session),
        ingame_id=participant.id.get(),
        refid=participant.refid.get(),
        name=participant.name.get(),
        is_ai=not participant.is_player.get(),
        vehicle=Vehicle.objects.get(ingame_id=participant.vehicle.get()),
        livery=Livery.objects.get(id_for_vehicle=participant.livery.get(), vehicle=vehicle),
    )
    participant.save(True)


def _make_snapshot(server, session):
    session_snapshot = SessionSnapshot(
        session=session,
        session_state=server.session.session_state.get(),
        session_stage=server.session.session_stage.get(),
        session_phase=server.session.session_phase.get(),
        session_time_elapsed=server.session.session_time_elapsed.get(),
        session_time_duration=server.session.session_time_duration.get(),
        num_participants_valid=server.session.num_participants_valid.get(),
        num_participants_disq=server.session.num_participants_disq.get(),
        num_participants_retired=server.session.num_participants_retired.get(),
        num_participants_dnf=server.session.num_participants_dnf.get(),
        num_participants_finished=server.session.num_participants_finished.get(),
        current_year=server.session.current_year.get(),
        current_month=server.session.current_month.get(),
        current_day=server.session.current_day.get(),
        current_hour=server.session.current_hour.get(),
        current_minute=server.session.current_minute.get(),
        rain_density_visual=server.session.rain_density_visual.get(),
        wetness_path=server.session.wetness_path.get(),
        wetness_off_path=server.session.wetness_off_path.get(),
        wetness_avg=server.session.wetness_avg.get(),
        wetness_predicted_max=server.session.wetness_predicted_max.get(),
        wetness_max_level=server.session.wetness_max_level.get(),
        temperature_ambient=server.session.temperature_ambient.get(),
        temperature_track=server.session.temperature_track.get(),
        air_pressure=server.session.air_pressure.get(),
    )
    session_snapshot.save(True)

    for it in server.members.elements:
        member_snapshot = MemberSnapshot(
            snapshot=session_snapshot,
            member=Member.objects.get(refid=it.refid.get(), session=session),
            load_state=it.load_state.get(),
            ping=it.ping.get(),
            index=it.index.get(),
            state=it.state.get(),
            join_time=it.join_time.get(),
            host=it.host.get(),
        )
        member_snapshot.save(True)

    for it in server.participants.elements:
        participant_snapshot = ParticipantSnapshot(
            snapshot=session_snapshot,
            participant=Participant.objects.get(ingame_id=it.id.get(), member__refid=it.refid.get(), member__session=session),
            grid_position=it.grid_position.get(),
            race_position=it.race_position.get(),
            current_lap=it.current_lap.get(),
            current_sector=it.current_sector.get(),
            sector1_time=it.sector1_time.get(),
            sector2_time=it.sector2_time.get(),
            sector3_time=it.sector3_time.get(),
            last_lap_time=it.last_lap_time.get(),
            fastest_lap_time=it.fastest_lap_time.get(),
            state=it.state.get(),
            headlights=it.headlights.get(),
            wipers=it.wipers.get(),
            speed=it.speed.get(),
            gear=it.gear.get(),
            rpm=it.rpm.get(),
            position_x=it.position_x.get(),
            position_y=it.position_y.get(),
            position_z=it.position_z.get(),
            orientation=it.orientation.get(),
        )
        participant_snapshot.save(True)

    return session_snapshot


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
            Livery(name=livery['name'], id_for_vehicle=livery['id'], vehicle_id=livery_vehicle.id).save(True)
