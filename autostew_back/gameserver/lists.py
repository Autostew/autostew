from enum import Enum


class ListName(Enum):
    events = 'events'
    tracks = 'tracks'
    vehicles = 'vehicles'
    game_modes = 'enums/game_mode'
    tire_wears = 'enums/tire_wear'
    penalties = 'enums/penalties'
    liveries = 'liveries'
    participant_attributes = 'attributes/participant'
    fuel_usages = 'enums/fuel_usage'
    vehicle_classes = 'vehicle_classes'
    session_attributes = 'attributes/session'
    allowed_views = 'enums/allowed_view'
    player_flags = 'flags/player'
    weathers = 'enums/weather'
    damage = 'enums/damage'
    member_attributes = 'attributes/member'
    session_flags = 'flags/session'


class ServerListItem:
    def __init__(self, raw):
        self.raw = raw


class Track(ServerListItem):
    def __init__(self, raw):
        ServerListItem.__init__(self, raw)
        self.gridsize = raw['gridsize']
        self.name = raw['name']
        self.id = raw['id']


class Event(ServerListItem):
    def __init__(self, raw):
        ServerListItem.__init__(self, raw)
        self.name = raw['name']
        self.type = raw['type']
        self.description = raw['description']
        self.attributes = raw['attributes']


class Vehicle(ServerListItem):
    def __init__(self, raw):
        ServerListItem.__init__(self, raw)
        self.name = raw['name']
        self.id = raw['id']
        self.class_name = raw['class']
        self.link_liveries = None
        self.link_class = None


class Livery(ServerListItem):
    def __init__(self, raw):
        ServerListItem.__init__(self, raw)
        self.name = raw['name']
        self.id = raw['id']
        self.class_name = raw['class']
        self.liveries = raw['liveries']  # TODO parse this


class NameValueItem(ServerListItem):
    def __init__(self, raw):
        ServerListItem.__init__(self, raw)
        self.name = raw['name']
        self.value = raw['value']


class AttributeItem(ServerListItem):
    def __init__(self, raw):
        ServerListItem.__init__(self, raw)
        self.name = raw['name']
        self.type = raw['type']
        self.access = raw['access']
        self.description = raw['description']


list_to_types = {
    ListName.events: {'ElemType': Event},
    ListName.tracks: {'ElemType': Track},
    ListName.vehicles: {'ElemType': Vehicle},
    ListName.game_modes: {'ElemType': NameValueItem},
    ListName.tire_wears: {'ElemType': NameValueItem},
    ListName.penalties: {'ElemType': NameValueItem},
    ListName.liveries: {'ElemType': Livery},
    ListName.participant_attributes: {'ElemType': AttributeItem},
    ListName.member_attributes: {'ElemType': AttributeItem},
    ListName.session_attributes: {'ElemType': AttributeItem},
    ListName.fuel_usages: {'ElemType': NameValueItem},
    ListName.vehicle_classes: {'ElemType': NameValueItem},
    ListName.allowed_views: {'ElemType': NameValueItem},
    ListName.player_flags: {'ElemType': NameValueItem},
    ListName.weathers: {'ElemType': NameValueItem},
    ListName.damage: {'ElemType': NameValueItem},
    ListName.session_flags: {'ElemType': NameValueItem},
}


class ServerList:
    def __init__(self, raw, elem_type):
        self.raw = raw
        self.description = raw.get('description', None)
        self.list = [elem_type(elem) for elem in self.raw['list']]

    def get_list_elements(self, key_field, key_value):
        result = []
        for elem in self.list:
            if elem.raw[key_field] == key_value:
                result.append(elem)
        return result


class ListGenerator:
    def __init__(self, api):
        self._api = api

    def generate_all(self):
        list_raw = self._api.get_lists()
        lists = {}
        for k, v in list_raw.items():
            list_name = ListName(k)
            lists[list_name] = ServerList(v, list_to_types[list_name]['ElemType'])
        self.create_links(lists)
        return lists

    def create_links(self, lists):
        for vehicle in lists[ListName.vehicles].list:
            vehicle.link_liveries = lists[ListName.liveries].get_list_elements('id', vehicle.id).pop().liveries
            vehicle.link_class = lists[ListName.vehicle_classes].get_list_elements('name', vehicle.class_name).pop()

        for vehicle_class in lists[ListName.vehicle_classes].list:
            vehicle_class.link_vehicles = lists[ListName.vehicles].get_list_elements('class', vehicle_class.name)

