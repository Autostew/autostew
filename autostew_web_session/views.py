from django.views import generic
from django.views.generic import FormView

from .models import Session, SessionSnapshot, Track
from .forms import SessionSetupForm


class ListTracks(generic.ListView):
    template_name = 'autostew_web_session/tracks.html'
    context_object_name = 'track_list'

    def get_queryset(self):
        return Track.objects.all().order_by('name')


class TrackView(generic.DetailView):
    model = Track
    template_name = 'autostew_web_session/track.html'


class CreateSessionView(FormView):
    template_name = 'autostew_web_session/create_form.html'
    form_class = SessionSetupForm
    success_url = '/session/all'


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


