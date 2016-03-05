
from django.views import generic

from autostew_web_session.models import Session, SessionSnapshot
from .models import Track


class IndexView(generic.ListView):
    template_name = 'autostew_web_session/tracks.html'
    context_object_name = 'track_list'

    def get_queryset(self):
        return Track.objects.all().order_by('name')


class DetailView(generic.DetailView):
    model = Track
    template_name = 'autostew_web_session/track.html'


class ListSessions(generic.ListView):
    template_name = 'autostew_web_session/sessions.html'
    context_object_name = 'session_list'

    def get_queryset(self):
        return Session.objects.all()


class SessionView(generic.DetailView):
    model = Session
    template_name = 'autostew_web_session/session.html'


class SnapshotView(generic.DetailView):
    model = SessionSnapshot
    template_name = 'autostew_web_session/snapshot.html'
