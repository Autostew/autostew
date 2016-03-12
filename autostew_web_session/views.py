import logging

from django.views import generic
from django.views.generic import FormView

from .models import Session, SessionSnapshot, Track
from .forms import SessionSetupForm


class Home(generic.TemplateView):
    template_name = 'autostew_web_session/home.html'


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

    def form_valid(self, form):
        logging.info("valid form data for session setup has been posted.")
        form.save()
        return super(CreateSessionView, self).form_valid(form)


class ListSessions(generic.ListView):
    template_name = 'autostew_web_session/sessions.html'
    context_object_name = 'session_list'

    def get_queryset(self):
        return Session.objects.all()


class SessionView(generic.DetailView):
    model = Session
    template_name = 'autostew_web_session/snapshot.html'

    def get_context_data(self, **kwargs):
        context = super(SessionView, self).get_context_data(**kwargs)
        # TODO get this as optional parameter, then delete SnapshotView
        context['sessionsnapshot'] = context['object'].current_snapshot
        return context


class SnapshotView(generic.DetailView):
    model = SessionSnapshot
    template_name = 'autostew_web_session/snapshot.html'

    def get_context_data(self, **kwargs):
        context = super(SnapshotView, self).get_context_data(**kwargs)
        context['session'] = context['object'].session
        return context
