# Monitor crashed
from autostew_back.gameserver.event import EventType, BaseEvent
from autostew_back.gameserver.server import Server as DedicatedServer

name = 'crash monitor'

crash_points_limit = 4000
crash_points = {}


def event(server: DedicatedServer, event: BaseEvent):
    global crash_points
    global crash_points_limit

    if event.type is EventType.impact and event.human_to_human:
            for participant in event.participants:
                steam_id = server.members.get_by_id(participant.refid).steam_id.get()
                crash_points[steam_id] = crash_points.setdefault(steam_id, 0) + event.magnitude
                if crash_points[steam_id] > crash_points_limit / 3:
                    participant.send_chat(
                        "WARNING: You have collected {points} crash points.".format(points=crash_points[steam_id])
                    )
                    participant.send_chat(
                        "Disqualification at {max_points} points.".format(max_crash_points=crash_points_limit)
                    )
                else:
                    participant.send_chat(
                        "Contact logged.".format(points=crash_points[steam_id])
                    )

