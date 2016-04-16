import datetime
from enum import Enum

from autostew_back.gameserver.participant import ParticipantState




class BaseEvent:
    reload_full_status = True

    def __init__(self, raw, server):
        self.server = server
        self.raw = raw
        self.type = EventType(raw['name'])
        self.index = raw['index']
        self.time = datetime.datetime.fromtimestamp(raw['time'])
        self.refid = raw.get('refid')
        self.participant_id = raw.get('participantid')


class MemberEvent(BaseEvent):
    def __init__(self, raw, server):
        BaseEvent.__init__(self, raw, server)
        self.member = self.server.members_api.get_by_id(raw['refid'])
        self.refid = raw['refid']


class ParticipantEvent(MemberEvent):
    def __init__(self, raw, server):
        MemberEvent.__init__(self, raw, server)
        self.participant = self.server.participants_api.get_by_id(raw['participantid'])
        self.refid = raw['refid']
        self.participant_id = raw['participantid']


class PlayerLeftEvent(MemberEvent):
    def __init__(self, raw, server):
        MemberEvent.__init__(self, raw, server)
        try:
            self.leaving_reason = LeavingReason(self.raw['attributes'].get('GameReasonId'))
        except ValueError as e:
            self.leaving_reason = None
        self.leaving_reason_str = raw['attributes'].get('Reason')


class PlayerJoinedEvent(MemberEvent):
    def __init__(self, raw, server):
        MemberEvent.__init__(self, raw, server)
        self.steam_id = raw['attributes']['SteamId']
        self.name = raw['attributes']['Name']


class StateChangedEvent(BaseEvent):
    def __init__(self, raw, server):
        BaseEvent.__init__(self, raw, server)
        self.previous_state = autostew_web_session.models.session_enums.SessionState(raw['attributes']['PreviousState'])
        self.new_state = autostew_web_session.models.session_enums.SessionState(raw['attributes']['NewState'])


class StageChangedEvent(BaseEvent):
    def __init__(self, raw, server):
        BaseEvent.__init__(self, raw, server)
        self.previous_stage = autostew_web_session.models.session_enums.SessionStage(raw['attributes']['PreviousStage'])
        self.new_stage = autostew_web_session.models.session_enums.SessionStage(raw['attributes']['NewStage'])
        self.new_stage_length = raw['attributes']['Length']


class SessionSetupEvent(BaseEvent):
    def __init__(self, raw, server):
        BaseEvent.__init__(self, raw, server)
        self.practice1_length = raw['attributes']['Practice1Length']
        self.practice2_length = raw['attributes']['Practice2Length']
        self.qualify_length = raw['attributes']['QualifyLength']
        self.warmup_length = raw['attributes']['WarmupLength']
        self.race1_length = raw['attributes']['Race1Length']
        self.race2_length = raw['attributes']['Race2Length']
        self.max_players = raw['attributes']['MaxPlayers']
        self.grid_size = raw['attributes']['GridSize']
        self.game_mode = raw['attributes']['GameMode']  # TODO parse this
        self.flags = raw['attributes']['Flags']  # TODO parse this
        self.track = raw['attributes']['TrackId']  # TODO parse this


class ParticipantCreatedEvent(ParticipantEvent):
    def __init__(self, raw, server):
        ParticipantEvent.__init__(self, raw, server)
        self.livery = raw['attributes']['LiveryId']  # TODO parse this
        self.vehicle = raw['attributes']['VehicleId']  # TODO parse this
        self.name = raw['attributes']['Name']
        self.is_player = raw['attributes']['IsPlayer'] == 1


class ParticipantStateEvent(ParticipantEvent):
    def __init__(self, raw, server):
        ParticipantEvent.__init__(self, raw, server)
        self.previous_state = ParticipantState(raw['attributes']['PreviousState'])
        self.new_state = ParticipantState(raw['attributes']['NewState'])


class SectorEvent(ParticipantEvent):
    def __init__(self, raw, server):
        ParticipantEvent.__init__(self, raw, server)
        self.count_this_lap = raw['attributes']['CountThisLap'] == 1
        self.sector_time = datetime.timedelta(milliseconds=raw['attributes']['SectorTime'])
        self.total_time = datetime.timedelta(milliseconds=raw['attributes']['TotalTime'])
        self.lap = raw['attributes']['Lap']
        self.sector = raw['attributes']['Sector'] + 1
        self.count_this_lap_times = raw['attributes']['CountThisLapTimes']


class LapEvent(ParticipantEvent):
    def __init__(self, raw, server):
        ParticipantEvent.__init__(self, raw, server)
        self.sector1_time = datetime.timedelta(milliseconds=raw['attributes']['Sector1Time'])
        self.sector2_time = datetime.timedelta(milliseconds=raw['attributes']['Sector2Time'])
        self.sector3_time = datetime.timedelta(milliseconds=raw['attributes']['Sector3Time'])
        self.distance_travelled = raw['attributes']['DistanceTravelled']
        self.race_position = raw['attributes']['RacePosition']
        self.lap = raw['attributes']['Lap']
        self.count_this_lap_times = raw['attributes']['CountThisLapTimes']
        self.lap_time = datetime.timedelta(milliseconds=raw['attributes']['LapTime'])


class PlayerChatEvent(BaseEvent):
    def __init__(self, raw, server):
        BaseEvent.__init__(self, raw, server)
        self.message = raw['attributes']['Message']


class ServerChatEvent(BaseEvent):
    def __init__(self, raw, server):
        BaseEvent.__init__(self, raw, server)
        self.message = raw['attributes']['Message']
        self.recipient = self.server.members_api.get_by_id(raw['attributes']['RefId'])


class ResultsEvent(ParticipantEvent):
    def __init__(self, raw, server):
        ParticipantEvent.__init__(self, raw, server)
        self.state = ParticipantState(raw['attributes']['State'])
        self.total_time = datetime.timedelta(milliseconds=raw['attributes']['TotalTime'])
        self.vehicle = raw['attributes']['VehicleId']  # TODO parse this
        self.fastest_lap_time = datetime.timedelta(milliseconds=raw['attributes']['FastestLapTime'])
        self.race_position = raw['attributes']['RacePosition']
        self.lap = raw['attributes']['Lap']


class ImpactEvent(ParticipantEvent):
    def __init__(self, raw, server):
        ParticipantEvent.__init__(self, raw, server)
        self.other_participant = self.server.participants_api.get_by_id(raw['attributes']['OtherParticipantId'])
        self.magnitude = raw['attributes']['CollisionMagnitude']

        self.participants = [self.participant]
        if self.other_participant is not None:
            self.participants.append(self.other_participant)

        self.human_to_human = (self.other_participant is not None and
                               self.participant.is_player.get() and
                               self.other_participant.is_player.get())


class CutTrackStartEvent(ParticipantEvent):
    def __init__(self, raw, server):
        ParticipantEvent.__init__(self, raw, server)
        self.lap_time = datetime.timedelta(milliseconds=raw['attributes']['LapTime'])
        self.is_main_branch = raw['attributes']['IsMainBranch'] == 1
        self.lap = raw['attributes']['Lap']
        self.race_position = raw['attributes']['RacePosition']


class CutTrackEndEvent(ParticipantEvent):
    def __init__(self, raw, server):
        ParticipantEvent.__init__(self, raw, server)
        self.elapsed_time = datetime.timedelta(milliseconds=raw['attributes']['ElapsedTime'])
        self.skipped_time = datetime.timedelta(milliseconds=raw['attributes']['SkippedTime'])
        self.place_gain = raw['attributes']['PlaceGain'] == 1
        self.penalty_threshold = raw['attributes']['PenaltyThreshold']
        self.penalty_value = raw['attributes']['PenaltyValue']


type_to_class = {
    EventType.session_setup: SessionSetupEvent,
    EventType.state_changed: StateChangedEvent,
    EventType.stage_changed: StageChangedEvent,
    EventType.session_created: BaseEvent,
    EventType.session_destroyed: BaseEvent,
    EventType.participant_state: ParticipantStateEvent,
    EventType.server_chat: ServerChatEvent,
    EventType.player_chat: PlayerChatEvent,
    EventType.player_joined: PlayerJoinedEvent,
    EventType.authenticated: MemberEvent,
    EventType.player_left: PlayerLeftEvent,
    EventType.participant_created: ParticipantCreatedEvent,
    EventType.participant_destroyed: BaseEvent,
    EventType.sector: SectorEvent,
    EventType.lap: LapEvent,
    EventType.results: ResultsEvent,
    EventType.cut_track_start: CutTrackStartEvent,
    EventType.cut_track_end: CutTrackEndEvent,
    EventType.impact: ImpactEvent,
}


def event_factory(raw, server):
    target_class = type_to_class[EventType(raw.get('name'))]
    return target_class(raw, server)
