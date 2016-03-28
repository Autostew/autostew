"""
Monitors crashes.
Can also be set to warn and kick crashing players.
"""

from autostew_back.gameserver.event import EventType, BaseEvent
from autostew_back.gameserver.participant import Participant
from autostew_back.gameserver.server import Server as DedicatedServer
from autostew_back.gameserver.session import SessionState

name = 'crash monitor'

ban_time = 600
crash_points_limit = 4000
crash_points = {}


def event(server: DedicatedServer, event: BaseEvent):
    if event.type == EventType.impact:
        for participant in event.participants:
            if participant.is_player.get():
                add_crash_points(
                    event.magnitude if event.human_to_human else int(event.magnitude / 4),
                    participant,
                    server
                )

    if event.type == EventType.state_changed and event.new_state == SessionState.lobby:
        reset_crash_points()


def reset_crash_points():
    global crash_points
    crash_points = {}


def add_crash_points(crash_points_increase: int, participant: Participant, server: DedicatedServer):
    steam_id = server.members.get_by_id(participant.refid.get()).steam_id.get()
    crash_points[steam_id] = crash_points.setdefault(steam_id, 0) + crash_points_increase
    participant.send_chat(
        "CONTACT logged for {points} points.".format(points=crash_points_increase),
        server
    )
    if crash_points[steam_id] > crash_points_limit:
        participant.kick(ban_time, server)
    elif crash_points[steam_id] > crash_points_limit / 3:
        participant.send_chat(
            "CONTACT WARNING: You have collected {points} crash points.".format(points=crash_points[steam_id]),
            server
        )
        participant.send_chat(
            "CONTACT WARNING: Disqualification at {max_crash_points} points.".format(max_crash_points=crash_points_limit),
            server
        )