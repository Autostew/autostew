from django.conf.urls import url

from autostew_web_account.views import login_view, account_view, logout_view, register_view, settings_view, \
    rotation_view, queue_view, add_view

urlpatterns = [
    url(r'^add$', add_view, name='add'),
    url(r'^settings/(?P<pk>[0-9]+)/?$', settings_view, name='settings'),
    url(r'^rotation/(?P<pk>[0-9]+)/?$', rotation_view, name='rotation'),
    url(r'^queue/(?P<pk>[0-9]+)/?$', queue_view, name='queue'),
    url(r'^register/?$', register_view, name='register'),
    url(r'^login/?$', login_view, name='login'),
    url(r'^logout/?$', logout_view, name='logout'),
    url(r'^$', account_view, name='home'),
]
