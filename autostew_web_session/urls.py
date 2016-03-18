from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from autostew_web_session.models import Track, Session
from . import views

app_name = 'session'
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='autostew_web_session/home.html'), name='home'),
    url(r'^tracks/?$', ListView.as_view(model=Track), name='tracks'),
    url(r'^tracks/(?P<pk>[0-9]+)/?$', DetailView.as_view(model=Track), name='track'),
    url(r'^sessions/?$', ListView.as_view(model=Session), name='sessions'),
    url(r'^create/?$', views.CreateSessionView.as_view(), name='create_session'),
    url(r'^session/(?P<pk>[0-9]+)/?$', views.session, name='session'),
    url(r'^session/(?P<pk>[0-9]+)/events/?$', views.SessionEvents.as_view(), name='events'),
    url(r'^session/(?P<pk>[0-9]+)/(?P<stage_name>[A-Za-z0-9]+)/?$', views.session_stage, name='session_stage'),
    url(r'^session/snapshot/(?P<pk>[0-9]+)/?$', views.SnapshotView.as_view(), name='snapshot'),
]
