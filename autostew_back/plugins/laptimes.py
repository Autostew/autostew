"""
Show a message when a fastest lap is finished.
"""
from autostew_back.gameserver.event import EventType, BaseEvent, LapEvent
from autostew_back.gameserver.server import Server
from autostew_back.utils import std_time_format

name = 'laptime announcements'

# Show laptime for every completed lap
announce_all = False
# Show a message when a new fastest lap is set
announce_fastest = True
# Show laptimes for leading car
announce_leading = 0

# Fastest lap time known
_fastest_known_lap_time = None


def event(server: Server, event: BaseEvent):
    global _fastest_known_lap_time

    # We reset the fastest lap at each stage change, like from practice to quali to race
    if event.type == EventType.stage_changed:
        reset_fastest_lap()

    # We announce new, valid laps
    if event.type == EventType.lap and event.count_this_lap_times:
        is_fastest_lap = check_if_new_fastest_lap(event)
        if lap_is_announcable(event):
            announce_lap(event, is_fastest_lap, server)


def announce_lap(event: LapEvent, is_fastest_lap: bool, server: Server):
    message = "{notice}P{position} - {participant} - {laptime}".format(
        notice="FASTEST LAP: " if is_fastest_lap else "",
        participant=event.participant.name.get(),
        laptime=std_time_format(event.lap_time),
        position=event.race_position,
    )
    server.api.send_chat("")
    server.api.send_chat(message)


def lap_is_announcable(event: LapEvent):
    """
    :param event: new LapEvent
    :return: True if new lap should be announced according to settings
    """
    return (
        announce_all or
        (announce_fastest and check_if_new_fastest_lap(event)) or
        (announce_leading >= event.race_position)
    )


def check_if_new_fastest_lap(event: LapEvent):
    """
    :param event: new LapEvent
    :return: True if new lap is fastest lap
    """
    global _fastest_known_lap_time

    if _fastest_known_lap_time is None or _fastest_known_lap_time >= event.lap_time:
        _fastest_known_lap_time = event.lap_time
        return True
    return False


def reset_fastest_lap():
    global _fastest_known_lap_time
    _fastest_known_lap_time = None
