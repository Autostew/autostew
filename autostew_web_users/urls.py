from django.conf.urls import url
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from autostew_web_users.models import SteamUser, SafetyClass
from autostew_web_users.views import SteamUserListView

app_name = 'users'
urlpatterns = [
    url(r'^list/?$', SteamUserListView.as_view(), name='list'),
    url(r'^safety_classes/?$', ListView.as_view(model=SafetyClass), name='safety_class_list'),
    url(r'^(?P<slug>.+)/?$', DetailView.as_view(model=SteamUser, slug_field='steam_id'), name='profile'),
]
