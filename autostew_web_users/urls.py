from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from autostew_web_users.models import SteamUser
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^list/?$', ListView.as_view(model=SteamUser), name='list'),
    url(r'^(?P<slug>.+)/?$', DetailView.as_view(model=SteamUser, slug_field='steam_id'), name='profile'),
]