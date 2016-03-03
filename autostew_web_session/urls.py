from django.conf.urls import url
from django.views.generic import ListView

from autostew_web_session.models import Track
from . import views

urlpatterns = [
    url(r'^$', ListView.as_view(
        queryset=Track.objects.all(),
        template_name="autostew_web_session/tracks.html")),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='track'),
]
