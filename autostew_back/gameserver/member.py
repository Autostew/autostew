from collections import Set
from enum import Enum

from autostew_back.gameserver.abstract_containers import AbstractAttribute, AbstractAttributeLinkedToList, \
    AbstractFlagAttribute, AbstractStatusTable, StatusList, AbstractAttributeLinkedToEnum
from autostew_back.gameserver.lists import ListName, AttributeItem


class MemberFlags(Enum):
    setup_used = 1
    controller_gamepad = 2
    controller_wheel = 4
    controller_mask = 6
    aid_steering = 8
    aid_braking = 16
    aid_abs = 32
    aid_traction = 64
    aid_stability = 128
    aid_no_damage = 256
    aid_auto_gears = 512
    aid_auto_clutch = 1024
    model_normal = 2048
    model_experienced = 4096
    model_pro = 6144
    model_elite = 8192
    model_mask = 14336
    aid_driving_line = 32768
    valid = 1073741824


class MemberLoadState(Enum):
    started_race = 'ADMIN_STARTED_RACE'
    ready = 'CLIENT_READY'
    unknown = 'UNKNOWN'


class MemberState(Enum):
    connected = 'Connected'


class MemberAttribute(AbstractAttribute):
    def __init__(self, descriptor, api, subsection='attributes'):
        AbstractAttribute.__init__(self, descriptor, api, subsection)
        self._writable = False
        self._writable_next_session = False


class MemberAttributeLinkedToList(AbstractAttributeLinkedToList):
    def __init__(self, descriptor, api, api_list, list_key, subsection='attributes'):
        AbstractAttributeLinkedToList.__init__(self, descriptor, api, api_list, list_key, subsection=subsection)
        self._writable = False
        self._writable_next_session = False


class MemberFlagAttribute(AbstractFlagAttribute):
    type_name_in_list = 'member'
    type_name_in_method = 'player'

    def __init__(self, descriptor, api, flags_enum, subsection='attributes'):
        AbstractFlagAttribute.__init__(self, descriptor, api, flags_enum, subsection)
        self._writable = False
        self._writable_next_session = False


class Member(AbstractStatusTable):
    def __init__(self, attr_list, lists, api):
        self._api = api
        self.attr_list = attr_list

        def _member_attribute(name):
            return MemberAttribute(self._from_list(name), api)

        self.vehicle = MemberAttributeLinkedToList(
            self._from_list('VehicleId'),
            api,
            lists[ListName.vehicles],
            'id'
        )
        self.livery = _member_attribute('LiveryId')
        self.load_state = AbstractAttributeLinkedToEnum(
            self._from_list('LoadState'),
            api,
            MemberLoadState,
            subsection='attributes'
        )
        self.race_stat_flags = MemberFlagAttribute(self._from_list('RaceStatFlags'), api, MemberFlags)
        self.ping = _member_attribute('Ping')

        self.index = MemberAttribute(AttributeItem({'name': 'index', 'access': 'ReadOnly', 'type': '', 'description': ''}), api, subsection=None)
        self.refid = MemberAttribute(AttributeItem({'name': 'refid', 'access': 'ReadOnly', 'type': '', 'description': ''}), api, subsection=None)
        self.steam_id = MemberAttribute(AttributeItem({'name': 'steamid', 'access': 'ReadOnly', 'type': '', 'description': ''}), api, subsection=None)
        self.state = AbstractAttributeLinkedToEnum(
            AttributeItem({'name': 'state', 'access': 'ReadOnly', 'type': '', 'description': ''}),
            api,
            MemberState,
            subsection=None
        )
        self.name = MemberAttribute(AttributeItem({'name': 'name', 'access': 'ReadOnly', 'type': '', 'description': ''}), api, subsection=None)
        self.join_time = MemberAttribute(AttributeItem({'name': 'jointime', 'access': 'ReadOnly', 'type': '', 'description': ''}), api, subsection=None)
        self.host = MemberAttribute(AttributeItem({'name': 'host', 'access': 'ReadOnly', 'type': '', 'description': ''}), api, subsection=None)

    def send_chat(self, message):
        self._api.send_chat(message, self.refid.get())


class MemberList(StatusList):
    def __init__(self, attr_list, lists, api):
        StatusList.__init__(self, attr_list, lists, api, Member, 'refid')
