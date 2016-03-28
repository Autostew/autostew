"""
Monitors crashes.
Can also be set to warn and kick crashing players.
"""

from autostew_back.gameserver.event import EventType, BaseEvent
from autostew_back.gameserver.participant import Participant
from autostew_back.gameserver.server import Server as DedicatedServer
from autostew_back.gameserver.session import SessionState


name = 'crash monitor'


warn_at = 0.7
ban_time = 0
crash_points_limit = 5000  # Set to zero to disable kicking
environment_crash_multiplier = 4
crash_points = {}


def event(server: DedicatedServer, event: BaseEvent):
    if event.type == EventType.impact:
        for participant in event.participants:
            if participant.is_player.get():
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


def add_crash_points(crash_points_increase: int, participant: Participant, server: DedicatedServer):
    steam_id = server.members.get_by_id(participant.refid.get()).steam_id.get()
    crash_points[steam_id] = crash_points.setdefault(steam_id, 0) + crash_points_increase

    participant.send_chat("", server)
    participant.send_chat(
        "CONTACT logged for {points} points.".format(points=crash_points_increase),
        server
    )

    if crash_points_limit and crash_points[steam_id] > crash_points_limit:
        participant.kick(server, ban_time)
    elif crash_points and crash_points[steam_id] > warn_at * crash_points_limit:
        participant.send_chat(
            "CONTACT: You have collected {points} crash points.".format(points=crash_points[steam_id]),
            server
        )
        participant.send_chat(
            "CONTACT: Disqualification at {max_crash_points} points.".format(max_crash_points=crash_points_limit),
            server
        )