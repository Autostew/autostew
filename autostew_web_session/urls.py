from django.conf.urls import url
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from autostew_web_session.models import Track
from autostew_web_session.views import ParticipantDetailView, SessionList
from . import views

app_name = 'session'
urlpatterns = [
    url(r'^tracks/?$', ListView.as_view(model=Track), name='tracks'),
    url(r'^tracks/(?P<pk>[0-9]+)/?$', DetailView.as_view(model=Track), name='track'),
    url(r'^list/?$', SessionList.as_view(), name='sessions'),
    url(r'^create/?$', views.CreateSessionView.as_view(), name='create_session'),
    url(r'^(?P<pk>[0-9]+)/?$', views.session, name='session'),
    url(r'^(?P<pk>[0-9]+)/events/?$', views.SessionEvents.as_view(), name='events'),
    url(r'^(?P<session_id>[0-9]+)/participant/(?P<participant_id>[0-9]+)/?$', ParticipantDetailView.as_view(), name='participant'),
    url(r'^(?P<pk>[0-9]+)/(?P<stage_name>[A-Za-z0-9]+)/?$', views.session_stage, name='session_stage'),
    url(r'^snapshot/(?P<pk>[0-9]+)/?$', views.SnapshotView.as_view(), name='snapshot'),
]
