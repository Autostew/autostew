from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, ParticipantState
from autostew_web_session.models.event import Event
from autostew_web_session.models.participant import Participant

warn_at = 0.7
environment_crash_multiplier = 0.1


class HandleCollision(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.impact and
            event.participant is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        magnitude = event.magnitude if event.human_to_human else int(event.magnitude * environment_crash_multiplier)
        if event.ai_involved:
            return
        if event.participant.state.name != ParticipantState.racing:
            return
        if event.other_participant and event.other_participant.state.name != ParticipantState.racing:
            return
        if event.participant.is_player:
            cls.add_crash_points(magnitude, event.participant, server, event.other_participant)
        if event.other_participant and event.other_participant.is_player:
            cls.add_crash_points(magnitude, event.other_participant, server, event.participant)

    @classmethod
    def add_crash_points(cls, crash_points_increase: int, participant: Participant, server, opponent: Participant=None):
        if opponent:
            crash_points_increase *= cls.get_interclass_multiplier(participant, opponent)

        participant.accumulated_crash_points += crash_points_increase
        participant.member.steam_user.add_crash_points(crash_points_increase)

        cls.crash_notification(crash_points_increase, participant, server, opponent)

        if participant.member.steam_user.over_class_kick_impact_threshold(crash_points_increase):
            participant.kick(server, server.back_crash_points_limit_ban_seconds)
        if server.back_crash_points_limit and participant.accumulated_crash_points > server.back_crash_points_limit:
            participant.kick(server, server.back_crash_points_limit_ban_seconds)
        elif server.back_crash_points_limit and participant.accumulated_crash_points > warn_at * server.back_crash_points_limit:
            cls.crash_limit_warning(participant, server)

    @classmethod
    def get_interclass_multiplier(cls, participant: Participant, opponent: Participant):
        if (
            opponent.member.steam_user.safety_class and
            opponent.member.steam_user.safety_class.impact_weight and
            participant.member.steam_user.safety_class and
            participant.member.steam_user.safety_class.impact_weight and
            participant.member.steam_user.safety_class.impact_weight < opponent.member.steam_user.safety_class.impact_weight
        ):
            return participant.member.steam_user.safety_class.impact_weight / opponent.member.steam_user.safety_class.impact_weight
        return 1

    @classmethod
    def crash_notification(cls, crash_points_increase, participant, server, opponent: Participant=None):
        participant.send_chat("", server)
        if opponent:
            participant.send_chat("CONTACT with {}".format(opponent.name), server)
        participant.send_chat("CONTACT logged for {points} points.".format(points=crash_points_increase), server)

    @classmethod
    def crash_limit_warning(cls, participant, server):
        participant.send_chat(
            "CONTACT: You have collected {points} crash points.".format(points=participant.accumulated_crash_points),
            server
        )
        participant.send_chat(
            "CONTACT: Disqualification at {max_crash_points} points.".format(max_crash_points=server.back_crash_points_limit),
            server
        )
