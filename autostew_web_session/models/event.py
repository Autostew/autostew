import datetime
import json
import logging

from django.db import models
from django.utils import timezone

from autostew_web_enums.models import SessionState, LeavingReason, SessionStage, GameModeDefinition, ParticipantState
from autostew_web_session.models.member import Member
from autostew_web_session.models.models import Track, Livery, Vehicle
from autostew_web_session.models.participant import Participant


class Event(models.Model):
    class Meta:
        ordering = ['ingame_index']

    session = models.ForeignKey('Session', null=True, blank=True)
    server = models.ForeignKey('Server', null=True, blank=True)
    type = models.ForeignKey('autostew_web_enums.EventType')
    timestamp = models.DateTimeField()
    ingame_index = models.IntegerField()
    raw = models.TextField()
    member = models.ForeignKey('Member', null=True, blank=True)
    recipient = models.ForeignKey('Member', null=True, blank=True, related_name='+')
    participant = models.ForeignKey('Participant', null=True, blank=True)
    other_participant = models.ForeignKey('Participant', null=True, blank=True, related_name='+')
    retries_remaining = models.SmallIntegerField(default=2)
    handled = models.BooleanField(default=False)

    def event_parse(self):
        jsonformatted_event = json.loads(self.raw)
        self.timestamp = timezone.make_aware(datetime.datetime.fromtimestamp(jsonformatted_event['time']))
        if 'refid' in jsonformatted_event.keys():
            try:
                self.member = self.get_member(jsonformatted_event['refid'])
                if 'participantid' in jsonformatted_event.keys():
                    self.participant = self.get_participant(jsonformatted_event['participantid'], jsonformatted_event['refid'])
            except (Member.DoesNotExist, Participant.DoesNotExist):
                pass
        if self.get_attribute('RefId'):
            try:
                self.recipient = self.get_member(self.get_attribute('RefId'))
            except Member.DoesNotExist:
                pass
        other_participant_id = self.get_attribute('OtherParticipantId')
        if other_participant_id and other_participant_id != -1:
            try:
                self.other_participant = self.get_participant(other_participant_id)
            except Participant.DoesNotExist:
                pass

    def get_attribute(self, name):
        return json.loads(self.raw)['attributes'].get(name)

    @property
    def race_position(self):
        return self.get_attribute('RacePosition')
    @property
    def new_session_state(self):
        return SessionState.get_or_create_default(name=self.get_attribute('NewState'))
    @property
    def previous_session_state(self):
        return SessionState.get_or_create_default(name=self.get_attribute('PreviousState'))
    @property
    def new_session_stage(self):
        return SessionStage.get_or_create_default(name=self.get_attribute('NewStage'))
    @property
    def previous_session_stage(self):
        return SessionStage.get_or_create_default(name=self.get_attribute('PreviousStage'))
    @property
    def leaving_reason(self):
        return LeavingReason.objects.get_or_create(
            ingame_id=self.get_attribute('GameReasonId'),
            defaults={'name': self.get_attribute('Reason')}
        )[0]
    @property
    def practice1_length(self):
        return self.get_attribute('Practice1Length')
    @property
    def practice2_length(self):
        return self.get_attribute('Practice2Length')
    @property
    def qualify_length(self):
        return self.get_attribute('QualifyLength')
    @property
    def warmup_length(self):
        return self.get_attribute('WarmupLength')
    @property
    def race1_length(self):
        return self.get_attribute('Race1Length')
    @property
    def race2_length(self):
        return self.get_attribute('Race2Length')
    @property
    def max_players(self):
        return self.get_attribute('MaxPlayers')
    @property
    def grid_size(self):
        return self.get_attribute('GridSize')
    @property
    def game_mode(self):
        return GameModeDefinition.get_or_create_default(self.get_attribute('GameMode'))
    @property
    def flags(self):
        return self.get_attribute('Flags')
    @property
    def track(self):
        return Track.get_or_create_default(self.get_attribute('TrackId'))
    @property
    def livery(self):
        return Livery.get_or_create_default(self.get_attribute('LiveryId'), self.vehicle)
    @property
    def vehicle(self):
        return Vehicle.get_or_create_default(self.get_attribute('VehicleId'))
    @property
    def name(self):
        return self.get_attribute('Name')
    @property
    def is_player(self):
        return self.get_attribute('IsPlayer') == 1
    @property
    def participant_state(self):
        return ParticipantState.get_or_create_default(self.get_attribute('State'))
    @property
    def previous_participant_state(self):
        return ParticipantState.get_or_create_default(self.get_attribute('PreviousState'))
    @property
    def new_participant_state(self):
        return ParticipantState.get_or_create_default(self.get_attribute('NewState'))
    @property
    def count_this_lap(self):
        return self.get_attribute('CountThisLap') == 1
    @property
    def sector_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('SectorTime'))
    @property
    def total_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('TotalTime'))
    @property
    def lap(self):
        return self.get_attribute('Lap')
    @property
    def sector(self):
        return self.get_attribute('Sector') + 1
    @property
    def count_this_lap_times(self):
        return self.get_attribute('CountThisLapTimes') == 1
    @property
    def sector1_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('Sector1Time'))
    @property
    def sector2_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('Sector2Time'))
    @property
    def sector3_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('Sector3Time'))
    @property
    def distance_travelled(self):
        return self.get_attribute('DistanceTravelled')
    @property
    def count_this_lap_times(self):
        return self.get_attribute('CountThisLapTimes') == 1
    @property
    def lap_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('LapTime'))
    @property
    def message(self):
        return self.get_attribute('Message')
    @property
    def fastest_lap_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('FastestLapTime'))
    @property
    def magnitude(self):
        return self.get_attribute('CollisionMagnitude')
    @property
    def is_main_branch(self):
        return self.get_attribute('IsMainBranch') == 1
    @property
    def elapsed_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('ElapsedTime'))
    @property
    def skipped_time(self):
        return datetime.timedelta(milliseconds=self.get_attribute('SkippedTime'))
    @property
    def place_gain(self):
        return self.get_attribute('PlaceGain') == 1
    @property
    def penalty_threshold(self):
        return self.get_attribute('PenaltyThreshold')
    @property
    def penalty_value(self):
        return self.get_attribute('PenaltyValue')
    @property
    def human_to_human(self):
        return (
            self.participant is not None and
            self.other_participant is not None and
            self.participant.is_player and
            self.other_participant.is_player
        )
    @property
    def ai_involved(self):
        if not self.participant.is_player:
            return True
        if self.other_participant and not self.other_participant.is_player:
            return True
        return False

    def handle(self, server):
        self.retries_remaining -= 1
        for handler in server.get_event_handlers():
            if handler.can_consume(server, self):
                handler.consume(server, self)
                self.handled = True
        self.save()
        if self.retries_remaining == 0 and not self.handled:
            logging.warning("Event could not be handled: {}".format(self.raw))