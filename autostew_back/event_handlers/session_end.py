from autostew_back.event_handlers.base_event_handler import BaseEventHandler
from autostew_web_enums.models import EventType, SessionState
from autostew_web_session.models.event import Event
from autostew_web_session.models.member import Member
from autostew_web_session.models.session import Session


class HandleSessionEnd(BaseEventHandler):

    @classmethod
    def can_consume(cls, server, event: Event):
        return (
            event.type.name == EventType.state_changed and
            event.new_session_state == SessionState.lobby and
            server.current_session is not None
        ) or (
            event.type.name == EventType.session_destroyed and
            server.current_session is not None
        )

    @classmethod
    def consume(cls, server, event: Event):
        if server.current_session.session_stage.is_relevant():
            server.current_session.finished = True
        server.current_session.running = False
        server.current_session.save()

        for member in server.current_session.member_set.all():
            member.steam_user.push_elo_rating()

        for member in server.current_session.get_members_who_participated():
            for opponent in server.current_session.get_members_who_participated():
                if member == opponent:
                    continue
                member.steam_user.update_elo_rating(
                    opponent.steam_user,
                    cls._versus_result(server.current_session, member, opponent)
                )

        server.current_session = None
        server.save()

    @classmethod
    def _versus_result(cls, session: Session, member: Member, opponent: Member) -> float:
        if not session.get_members_who_finished_race():
            return None
        member_stayed = member in session.get_members_who_finished_race()
        opponent_stayed = opponent in session.get_members_who_finished_race()

        if not member_stayed and not opponent_stayed:
            return 0.5
        if member_stayed and not opponent_stayed:
            return 1
        if opponent_stayed and not member_stayed:
            return 0
        if member_stayed and opponent_stayed:
            if member.get_participant(session).race_position < opponent.get_participant(session).race_position:
                return 1
            else:
                return 0
