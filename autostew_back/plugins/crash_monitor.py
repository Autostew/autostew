"""
Monitors crashes.
Can also be set to warn and kick crashing players.
"""

from autostew_back.gameserver.event import EventType, BaseEvent
from autostew_back.gameserver.participant import Participant
from autostew_web_session.models.session_enums import SessionState
from autostew_back.plugins.db_session_writer_libs import db_safety_rating
from autostew_web_session.models.server import Server
from autostew_web_users.models import SteamUser, SafetyClass

name = 'crash monitor'


warn_at = 0.7
ban_time = 0
crash_points_limit = 4000  # Set to zero to disable kicking
environment_crash_multiplier = 4
crash_points = {}


def event(server: Server, event: BaseEvent):
    if event.type == EventType.impact:
        for participant in event.participants:
            if participant and participant.is_player.get():
                add_crash_points(
                    event.magnitude if event.human_to_human else int(event.magnitude / environment_crash_multiplier),
                    participant,
                    server
                )

    if event.type == EventType.state_changed and event.new_state == SessionState.lobby:
        reset_crash_points()


def reset_crash_points():
    global crash_points
    crash_points = {}


def add_crash_points(
        crash_points_increase: int,
        participant: Participant,
        server: Server,
        opponent: Participant=None
):
    if not participant:
        return
    steam_id = server.members_api.get_by_id(participant.refid.get()).steam_id.get()
    crash_points[steam_id] = crash_points.setdefault(steam_id, 0) + crash_points_increase

    opponent_user = None
    if opponent and opponent.get_member(server):
        try:
            opponent_user = SteamUser.objects.get(steam_id=opponent.get_member(server).steam_id.get())
        except SteamUser.DoesNotExist:
            pass

    try:
        steam_user = SteamUser.objects.get(steam_id=participant.get_member(server).steam_id.get())
    except SteamUser.DoesNotExist:
        steam_user = None

    if (
            opponent_user and
            opponent_user.safety_class and
            opponent_user.safety_class.impact_weight and
            steam_user.safety_class and
            steam_user.safety_class.impact_weight and
            steam_user.safety_class.impact_weight < opponent_user.safety_class.impact_weight
    ):
        crash_points_increase *= (
            steam_user.safety_class.impact_weight / opponent_user.safety_class.impact_weight
        )

    db_safety_rating.impact(steam_user, crash_points_increase)
    if steam_user.over_class_kick_impact_threshold(crash_points_increase):
        participant.kick(server, ban_time)

    crash_notification(crash_points_increase, participant, server)

    if crash_points_limit and crash_points[steam_id] > crash_points_limit:
        participant.kick(server, ban_time)
    elif crash_points_limit and crash_points[steam_id] > warn_at * crash_points_limit:
        crash_limit_warning(participant, server, steam_id)


def crash_notification(crash_points_increase, participant, server):
    participant.send_chat("", server)
    participant.send_chat(
        "CONTACT logged for {points} points.".format(points=crash_points_increase),
        server
    )


def crash_limit_warning(participant, server, steam_id):
    participant.send_chat(
        "CONTACT: You have collected {points} crash points.".format(points=crash_points[steam_id]),
        server
    )
    participant.send_chat(
        "CONTACT: Disqualification at {max_crash_points} points.".format(max_crash_points=crash_points_limit),
        server
    )
