from rest_framework import viewsets

from autostew_web_api.serializers import SessionSerializer
from autostew_web_session.models.session import Session


class SessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sessions to be viewed or edited.
    """
    queryset = Session.objects.all().order_by('timestamp')
    serializer_class = SessionSerializer
