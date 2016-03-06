from django.conf.urls import url

from . import views

app_name = 'session'
urlpatterns = [
    url(r'^all/?$', views.ListSessions.as_view(), name='sessions'),
    url(r'^(?P<pk>[0-9]+)/?$', views.SessionView.as_view(), name='session'),
    url(r'^snapshot/(?P<pk>[0-9]+)/?$', views.SnapshotView.as_view(), name='snapshot'),
    url(r'^create/?$', views.CreateSessionView.as_view(), name='create_session'),
]
