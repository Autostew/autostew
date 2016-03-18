import logging

from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import FormView

from autostew_web_enums.models import SessionStage
from autostew_web_session import models
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


def session_stage(request, pk, stage_name):
    session = get_object_or_404(Session, pk=pk)
    if session.current_snapshot.session_stage.name == stage_name:
        target_snapshot = session.current_snapshot
    else:
        stage = get_object_or_404(models.SessionStage, session=session, stage__name=stage_name)
        if stage.result_snapshot:
            target_snapshot = stage.result_snapshot
        else:
            target_snapshot = stage.starting_snapshot  # TODO should be get_latest_snapshot_in_stage
    return SnapshotView.as_view()(request, pk=target_snapshot.id)


def session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    return SnapshotView.as_view()(request, pk=session.current_snapshot_id)


class SnapshotView(generic.DetailView):
    model = SessionSnapshot
    template_name = 'autostew_web_session/snapshot.html'

    def get_context_data(self, **kwargs):
        context = super(SnapshotView, self).get_context_data(**kwargs)
        context['session'] = context['object'].session
        return context
