from rest_framework import viewsets

from autostew_web_api.serializers import SessionSerializer
from autostew_web_session.models.session import Session


class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
