from enum import Enum


class SessionFlags(Enum):
    force_identical_vehicles = 2
    allow_custom_vehicle_setup = 8
    force_realistic_driving_aids = 16
    abs_allowed = 32
    sc_allowed = 64
    tcs_allowed = 128
    force_manual = 256
    rolling_starts = 512
    force_same_vehicle_class = 1024
    fill_session_with_ai = 131072
    mechanical_failures = 262144
    auto_start_engine = 524288
    timed_race = 1048576
    ghost_griefers = 2097152
    enforced_pitstop = 4194304


class SessionState(Enum):
    none = 'None'
    lobby = 'Lobby'
    loading = 'Loading'
    race = 'Race'
    post_race = 'PostRace'
    returning = 'Returning'


class SessionStage(Enum):
    practice1 = 'Practice1'
    practice2 = 'Practice2'
    qualifying = 'Qualifying'
    warmup = 'Warmup'
    formationlap = 'FormationLap'
    race1 = 'Race1'


class SessionPhase(Enum):
    pre_countdown_sync = 'PreCountDownSync'
    prerace = 'PreRace'
    countdown_wait = 'CountDownWait'
    countdown = 'CountDown'
    green = 'Green'
    invalid = 'Invalid'


class Privacy(Enum):
    public = 0
    friends = 1
    private = 2