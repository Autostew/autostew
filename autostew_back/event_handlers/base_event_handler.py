from autostew_web_session.models.event import Event


class BaseEventHandler:

    @classmethod
    def can_consume(cls, server, event: Event):
        return False

    @classmethod
    def consume(cls, server, event: Event):
        pass
