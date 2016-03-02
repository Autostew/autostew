# Monitor crashed
from autostew_back.gameserver.event import EventType

name = 'crash monitor'

crash_points_limit = 4000
crash_points = {}

def tick(server):
    pass


def event(server, event):
    global crash_points
    global crash_points_limit

    if event.type is EventType.impact and event.human_to_human:
            for participant in event.participants:
                steam_id = participant.member.steam_id.get()
                crash_points[steam_id] = crash_points.setdefault(steam_id, 0) + event.magnitude
                if crash_points[steam_id] > crash_points_limit / 2:
                    participant.send_chat(
                        "WARNING: You have collected {points} crash points.".format(points=crash_points[steam_id])
                    )
                    participant.send_chat(
                        "You will be kicked at {max_points} crash points.".format(max_crash_points=crash_points_limit)
                    )
                else:
                    participant.send_chat(
                        "Contact logged.".format(points=crash_points[steam_id])
                    )

