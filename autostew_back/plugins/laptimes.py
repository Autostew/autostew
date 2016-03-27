"""
Show a message when a fastest lap is finished.
"""
from autostew_back.gameserver.event import EventType, BaseEvent
from autostew_back.gameserver.server import Server
from autostew_back.utils import std_time_format

name = 'laptime announcements'

# Show laptime for every completed lap
show_always = False
# Show a message when a new fastest lap is set
show_fastest = True
# Show laptimes for leading car
show_leading_cars = 0

# Internal variables
_fastest_lap_time = None


def tick(server):
    pass


def event(server: Server, event: BaseEvent):
    global _fastest_lap_time
    if event.type == EventType.stage_changed:
        _fastest_lap_time = None
    if event.type == EventType.lap and event.count_this_lap_times:
        is_fastest_lap = False

        if _fastest_lap_time is None or _fastest_lap_time > event.lap_time:
            _fastest_lap_time = event.lap_time
            is_fastest_lap = True

        if (
                show_always or
                (show_fastest and is_fastest_lap) or
                (show_leading_cars >= event.race_position)
        ):
            server.api.send_chat(
                "{notice}P{position} - {participant} - {laptime}".format(
                    participant=event.participant.name.get(),
                    laptime=std_time_format(event.lap_time),
                    position=event.race_position,
                    notice="FASTEST LAP: " if is_fastest_lap else ""
                )
            )
