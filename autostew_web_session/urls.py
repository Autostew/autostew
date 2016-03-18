from django.conf.urls import url

from . import views

app_name = 'session'
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^tracks/?$', views.ListTracks.as_view(), name='tracks'),
    url(r'^tracks/(?P<pk>[0-9]+)/?$', views.TrackView.as_view(), name='track'),
    url(r'^sessions/?$', views.ListSessions.as_view(), name='sessions'),
    url(r'^create/?$', views.CreateSessionView.as_view(), name='create_session'),
    url(r'^session/(?P<pk>[0-9]+)/?$', views.session, name='session'),
    url(r'^session/(?P<pk>[0-9]+)/(?P<stage_name>[A-Za-z0-9]+)/?$', views.session_stage, name='session_stage'),
    url(r'^session/snapshot/(?P<pk>[0-9]+)/?$', views.SnapshotView.as_view(), name='snapshot'),
]
