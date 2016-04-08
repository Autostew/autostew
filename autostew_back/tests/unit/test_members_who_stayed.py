import datetime

import pytz
from django.test.testcases import TestCase
from django.utils import timezone

from autostew_back.plugins.db_session_writer_libs import db_elo_rating
from autostew_back.tests.unit.test_plugin_db_writer import TestDBWriter
from autostew_web_enums.models import ParticipantState
from autostew_web_session.models.models import SessionSetup, Session, Member, Vehicle, VehicleClass, Livery, \
    SessionStage, SessionSnapshot, MemberSnapshot, Participant, ParticipantSnapshot, Lap
from autostew_web_session.models.server import Server
from autostew_web_users.models import SteamUser
from autostew_web_enums import models as enum_models


class TestMembersWhoStayed(TestCase):

    def create_test_session(self, server: Server, setup: SessionSetup) -> Session:
        return Session(
            server=server,
            setup_template=setup,
            setup_actual=setup,
            planned=False,
            running=True,
            finished=False,
        )

    def create_test_server(self) -> Server:
        return Server(
            name = "testserver",
            setup_rotation_index=0,
            running=True,
            last_ping=timezone.make_aware(datetime.datetime.now()),
            average_player_latency=42
        )

    def test_members_who_stayed(self):
        server = self.create_test_server()
        server.save()
        test_setup = TestDBWriter.make_test_setup()
        test_setup.save()
        session = self.create_test_session(server, test_setup)
        session.save()
        server.current_session = session
        server.save()
        user1 = SteamUser.objects.create(display_name='player1')
        user2 = SteamUser.objects.create(display_name='player2')
        user3 = SteamUser.objects.create(display_name='player3')
        vehicle = Vehicle.objects.create(
            name="FooCar",
            ingame_id=1,
            vehicle_class=VehicleClass.objects.create(name="FooCars", ingame_id=2)
        )
        livery = Livery.objects.create(
            name="Livery",
            id_for_vehicle=3,
            vehicle=vehicle
        )
        member1 = self.create_test_member("Alice", session, user1, vehicle, livery)
        member2 = self.create_test_member("Bob", session, user2, vehicle, livery)
        member3 = self.create_test_member("Carol", session, user3, vehicle, livery)
        participant1 = Participant.objects.create(
            member=member1,
            session=session,
            still_connected=True,
            ingame_id=1,
            refid=1,
            name="Alice",
            is_ai=False,
            vehicle=vehicle,
            livery=livery
        )
        participant2 = Participant.objects.create(
            member=member2,
            session=session,
            still_connected=True,
            ingame_id=2,
            refid=1,
            name="Bob",
            is_ai=False,
            vehicle=vehicle,
            livery=livery
        )
        final_snapshot = SessionSnapshot.objects.create(
            session=session,
            is_result=True,
            session_state=enum_models.SessionState.objects.create(name="PostRace"),
            session_stage=enum_models.SessionStage.objects.create(name="Race1"),
            session_phase=enum_models.SessionPhase.objects.create(name="Phase"),
            session_time_elapsed=1200,
            session_time_duration=1200,
            num_participants_valid=1,
            num_participants_disq=0,
            num_participants_retired=0,
            num_participants_dnf=0,
            num_participants_finished=1,
            current_year=0,
            current_month=0,
            current_day=0,
            current_hour=0,
            current_minute=0,
            rain_density_visual=0,
            wetness_path=0,
            wetness_off_path=0,
            wetness_avg=0,
            wetness_predicted_max=0,
            wetness_max_level=0,
            temperature_ambient=0,
            temperature_track=0,
            air_pressure=0,
        )
        final_stage = SessionStage.objects.create(
            session=session,
            stage=enum_models.SessionStage.objects.get_or_create(name="Race1")[0],
            result_snapshot=final_snapshot
        )
        membersnapshot = MemberSnapshot.objects.create(
            member=member1,
            snapshot=final_snapshot,
            still_connected=True,
            load_state=enum_models.MemberLoadState.objects.get_or_create(name="Blub")[0],
            ping=42,
            index=1,
            state=enum_models.MemberState.objects.get_or_create(name="Blab")[0],
            join_time=1,
            host=False
        )
        membersnapshot.save()
        participant_snapshot = ParticipantSnapshot(
            snapshot=final_snapshot,
            participant=participant1,
            still_connected=True,
            grid_position=0,
            race_position=1,
            current_lap=0,
            current_sector=0,
            sector1_time=0,
            sector2_time=0,
            sector3_time=0,
            last_lap_time=0,
            fastest_lap_time=0,
            state = ParticipantState.objects.create(name="State"),
            headlights=0,
            wipers=0,
            speed=0,
            gear=0,
            rpm=0,
            position_x=0,
            position_y=0,
            position_z=0,
            orientation=0,
            total_time=0,
        )
        participant_snapshot.save()

        lap1 = Lap.objects.create(
            session=session,
            session_stage=final_stage.stage,
            participant=participant1,
            lap=1,
            count_this_lap=True,
            position=1,
            lap_time=1337,
            sector1_time=1337,
            sector2_time=1337,
            sector3_time=1337,
            distance_travelled=1337,
        )
        lap2 = Lap.objects.create(
            session=session,
            session_stage=final_stage.stage,
            participant=participant2,
            lap=1,
            count_this_lap=True,
            position=1,
            lap_time=1337,
            sector1_time=1337,
            sector2_time=1337,
            sector3_time=1337,
            distance_travelled=1337,
        )

        self.assertEqual(len(session.get_members_who_finished_race()), 1)
        self.assertEqual(session.get_members_who_finished_race()[0].name, "Alice")
        self.assertEqual(len(session.member_set.all()), 3)
        self.assertEqual(db_elo_rating._versus_result(session, member1, member2), 1)
        self.assertEqual(db_elo_rating._versus_result(session, member1, member3), 1)
        self.assertEqual(db_elo_rating._versus_result(session, member2, member1), 0)
        self.assertEqual(db_elo_rating._versus_result(session, member3, member1), 0)
        self.assertEqual(db_elo_rating._versus_result(session, member2, member3), 0.5)
        self.assertEqual(db_elo_rating._versus_result(session, member3, member2), 0.5)
        self.assertEqual(session.get_race_stage(), final_stage)
        self.assertEqual(member1.finishing_position(), 1)
        db_elo_rating.update_ratings_after_race_end(session)
        user1.refresh_from_db()
        user2.refresh_from_db()
        user3.refresh_from_db()
        self.assertEqual(user1.elo_rating, 1002)
        self.assertEqual(user2.elo_rating, 998)
        self.assertEqual(user3.elo_rating, 1000)
        self.assertEqual(len(session.get_members_who_participated()), 2)

    def create_test_member(self, name, session, user1, vehicle, livery) -> Member:
        return Member.objects.create(
            steam_user=user1,
            session=session,
            still_connected=True,
            vehicle=vehicle,
            livery=livery,
            refid=1,
            name=name,
            setup_used=False,
            controller_gamepad=False,
            controller_wheel=False,
            aid_steering=False,
            aid_braking=False,
            aid_abs=False,
            aid_traction=False,
            aid_stability=False,
            aid_no_damage=False,
            aid_auto_gears=False,
            aid_auto_clutch=False,
            model_normal=False,
            model_experienced=False,
            model_pro=False,
            model_elite=False,
            aid_driving_line=False,
            valid=True,
        )

