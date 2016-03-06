from django.conf.urls import include, url
from django.contrib import admin

from autostew_web_session.views import ListTracks, TrackView

urlpatterns = [
    url(r'^session/', include('autostew_web_session.urls')),
    url(r'^tracks/$', ListTracks.as_view(), name='tracks'),
    url(r'^tracks/(?P<pk>[0-9]+)/?$', TrackView.as_view(), name='track'),
    url(r'^admin/', admin.site.urls, name='admin'),
]
