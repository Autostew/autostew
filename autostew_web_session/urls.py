from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from autostew_web_session.models.models import Track
from autostew_web_session.models.session import SessionSetup, Session
from autostew_web_session.models.server import Server
from autostew_web_session.views import ParticipantDetailView, SessionList, TrackDetailView, SessionView
from . import views

app_name = 'session'
urlpatterns = [
    url(r'^tracks/?$', ListView.as_view(model=Track), name='tracks'),
    url(r'^tracks/(?P<pk>[0-9]+)/?$', TrackDetailView.as_view(), name='track'),
    url(r'^list/?$', SessionList.as_view(), name='sessions'),
    url(r'^servers/?$', ListView.as_view(model=Server), name='servers'),
    url(r'^servers/(?P<slug>.+)/?$', DetailView.as_view(model=Server, slug_field='name'), name='server'),
    url(r'^(?P<pk>[0-9]+)/?$', SessionView.as_view(), name='session'),
    url(r'^(?P<pk>[0-9]+)/events/?$', views.SessionEvents.as_view(), name='events'),
    url(r'^(?P<session_id>[0-9]+)/participant/(?P<participant_id>[0-9]+)/?$', ParticipantDetailView.as_view(), name='participant'),
    url(r'^(?P<pk>[0-9]+)/(?P<stage_name>[A-Za-z0-9]+)/?$', views.session_stage, name='session_stage'),
    url(r'^snapshot/(?P<pk>[0-9]+)/?$', SessionView.as_view(), name='snapshot'),
    url(r'^setup/create/?$', login_required(views.CreateSessionView.as_view()), name='create_setup'),
    url(r'^setup/list/?$', ListView.as_view(model=SessionSetup, queryset=SessionSetup.objects.filter(is_template=True)), name='setups'),
    url(r'^setup/(?P<pk>[0-9]+)/?$', DetailView.as_view(model=SessionSetup), name='setup'),
]
