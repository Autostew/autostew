import logging

from django.db.models.aggregates import Min
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic import FormView

from autostew_web_session import models
from autostew_web_session.models import Event, Participant, SessionSetup, Server, Track, Vehicle, VehicleClass, Lap
from .models import Session, SessionSnapshot
from .forms import SessionSetupForm


class CreateSessionView(FormView):
    template_name = 'autostew_web_session/create_form.html'
    form_class = SessionSetupForm
    success_url = '/session/all'

    def form_valid(self, form):
        logging.debug("valid form data for session setup has been posted.")
        form.save()
        return super(CreateSessionView, self).form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super(SnapshotView, self).get_context_data(**kwargs)
        context['session'] = context['object'].session
        return context


class SessionEvents(generic.ListView):
    model = Event

    def get_queryset(self):
        self.session = get_object_or_404(Session, id=self.kwargs['pk'])
        return self.session.event_set.all()

    def get_context_data(self, **kwargs):
        context = super(SessionEvents, self).get_context_data(**kwargs)
        context['session'] = self.session
        return context


class SessionList(generic.ListView):
    model = Session

    def get_context_data(self, **kwargs):
        context = super(SessionList, self).get_context_data(**kwargs)
        context['sessions_in_progress'] = Session.objects.filter(running=True, finished=False)
        context['sessions_planned'] = Session.objects.filter(planned=True, running=False, finished=False)
        context['sessions_history'] = Session.objects.filter(finished=True).order_by('-id')[:10]
        context['setups_in_rotation'] = SessionSetup.objects.filter(rotated_in_server=Server.objects.all())
        return context


class ParticipantDetailView(generic.DetailView):
    model = Participant

    def get_object(self, queryset=None):
        return get_object_or_404(
            Participant,
            session__id=self.kwargs['session_id'],
            ingame_id=self.kwargs['participant_id']
        )


class TrackDetailView(generic.DetailView):
    model = Track

    def get_context_data(self, **kwargs):
        context = super(TrackDetailView, self).get_context_data(**kwargs)
        context['vehicle_classes'] = VehicleClass.objects.all()
        context['vehicles'] = Vehicle.objects.all()
        if self.request.GET.get('vehicle'):
            context['vehicle'] = get_object_or_404(Vehicle, ingame_id=self.request.GET.get('vehicle'))
            context['laps'] = Lap.objects.filter(
                session__setup_actual__track=context['object'],
                participant__vehicle=context['vehicle'],
                count_this_lap=True,
                participant__is_ai=False,
            ).values('participant').annotate(fastest_lap_time=Min('lap_time'))
        elif self.request.GET.get('vehicle_class'):
            context['vehicle_class'] = get_object_or_404(VehicleClass, ingame_id=self.request.GET.get('vehicle_class'))
            context['laps'] = Lap.objects.filter(
                session__setup_actual__track=context['object'],
                participant__vehicle__vehicle_class=context['vehicle_class'],
                count_this_lap=True,
                participant__is_ai=False,
            ).values('participant').annotate(fastest_lap_time=Min('lap_time'))
        else:
            context['laps'] = []
        return context
