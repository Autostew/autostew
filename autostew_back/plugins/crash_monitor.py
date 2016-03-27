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
    global crash_points

    if event.type is EventType.impact:
        for participant in event.participants:
            add_crash_points(
                event.magnitude if event.human_to_human else event.magnitude / 4,
                participant,
                server
            )

    if event.type == EventType.state_changed and event.new_state == SessionState.lobby:
        crash_points = {}


def add_crash_points(crash_points_increase: int, participant: Participant, server: DedicatedServer):
    steam_id = server.members.get_by_id(participant.refid.get()).steam_id.get()
    crash_points[steam_id] = crash_points.setdefault(steam_id, 0) + crash_points_increase
    participant.send_chat(
        "CONTACT logged for {points} points.".format(points=crash_points[steam_id])
    )
    if crash_points[steam_id] > crash_points_limit:
        participant.kick(ban_time)
    elif crash_points[steam_id] > crash_points_limit / 3:
        participant.send_chat(
            "CONTACT WARNING: You have collected {points} crash points.".format(points=crash_points[steam_id])
        )
        participant.send_chat(
            "CONTACT WARNING: Disqualification at {max_crash_points} points.".format(max_crash_points=crash_points_limit)
        )