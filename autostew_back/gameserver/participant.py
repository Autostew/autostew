from enum import Enum

from autostew_back.gameserver.abstract_containers import AbstractAttribute, AbstractAttributeLinkedToList, \
    AbstractStatusTable, StatusList
from autostew_back.gameserver.lists import ListName, AttributeItem


class ParticipantStates(Enum):
    racing = 'Racing'
    finished = 'Finished'
    dnf = 'DNF'
    disqualified = 'Disqualified'
    retired = 'Retired'
    in_garage = 'InGarage'
    entering_pits = 'EnteringPits'
    in_pits = 'InPits'
    exiting_pits = 'ExitingPits'


class ParticipantAttribute(AbstractAttribute):
    def __init__(self, descriptor, api, subsection='attributes'):
        AbstractAttribute.__init__(self, descriptor, api, subsection)
        self._writable = False
        self._writable_next_session = False


class ParticipantAttributeLinkedToList(AbstractAttributeLinkedToList):
    def __init__(self, descriptor, api, api_list, list_key, subsection='attributes'):
        AbstractAttributeLinkedToList.__init__(self, descriptor, api, api_list, list_key, subsection=subsection)
        self._writable = False
        self._writable_next_session = False


class Participant(AbstractStatusTable):
    def __init__(self, attr_list, lists, api):
        self._api = api
        self.attr_list = attr_list
        self.id = ParticipantAttribute(
            AttributeItem({'name': 'id', 'access': 'ReadOnly', 'type': '', 'description': ''}),
            api, subsection=None)

        def _member_attribute(name):
            return ParticipantAttribute(self._from_list(name), api)

        self.refid = _member_attribute('RefId')
        self.name = _member_attribute('Name')
        self.is_player = _member_attribute('IsPlayer')
        self.grid_position = _member_attribute('GridPosition')
        self.vehicle = ParticipantAttributeLinkedToList(
            self._from_list('VehicleId'),
            api,
            lists[ListName.vehicles],
            'id'
        )
        self.livery = _member_attribute('LiveryId')
        self.race_position = _member_attribute('RacePosition')
        self.current_lap = _member_attribute('CurrentLap')
        self.current_sector = _member_attribute('CurrentSector')
        self.sector1_time = _member_attribute('Sector1Time')
        self.sector2_time = _member_attribute('Sector2Time')
        self.sector3_time = _member_attribute('Sector3Time')
        self.last_lap_time = _member_attribute('LastLapTime')
        self.fastest_lap_time = _member_attribute('FastestLapTime')
        self.state = _member_attribute('State')
        self.headlights = _member_attribute('HeadlightsOn')
        self.wipers = _member_attribute('WipersOn')
        self.speed = _member_attribute('Speed')
        self.gear = _member_attribute('Gear')
        self.rpm = _member_attribute('RPM')
        self.position_x = _member_attribute('PositionX')
        self.position_y = _member_attribute('PositionY')
        self.position_z = _member_attribute('PositionZ')
        self.orientation = _member_attribute('Orientation')

    def send_chat(self, message):
        self.member.send_chat(message)


class ParticipantList(StatusList):
    def __init__(self, attr_list, lists, api):
        StatusList.__init__(self, attr_list, lists, api, Participant, 'id')
