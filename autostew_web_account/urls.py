from django.conf.urls import url

from autostew_web_account.views import login_view, account_view, logout_view, register_view, settings_view, \
    rotation_view, queue_view, add_view, remove_rotated_setup, add_setup_to_rotation, remove_queued_setup, \
    add_setup_to_queue

urlpatterns = [
    url(r'^add$', add_view, name='add'),
    url(r'^settings/(?P<pk>[0-9]+)/?$', settings_view, name='settings'),
    url(r'^rotation/(?P<pk>[0-9]+)/?$', rotation_view, name='rotation'),
    url(r'^rotation/(?P<server_pk>[0-9]+)/remove/(?P<entry_pk>[0-9]+)/?$', remove_rotated_setup, name='remove_rotated_setup'),
    url(r'^rotation/(?P<server_pk>[0-9]+)/add/(?P<setup_pk>[0-9]+)/?$', add_setup_to_rotation, name='add_setup_to_rotation'),
    url(r'^queue/(?P<pk>[0-9]+)/?$', queue_view, name='queue'),
    url(r'^queue/(?P<server_pk>[0-9]+)/remove/(?P<entry_pk>[0-9]+)/?$', remove_queued_setup, name='remove_queued_setup'),
    url(r'^queue/(?P<server_pk>[0-9]+)/add/(?P<setup_pk>[0-9]+)/?$', add_setup_to_queue, name='add_setup_to_queue'),
    url(r'^register/?$', register_view, name='register'),
    url(r'^login/?$', login_view, name='login'),
    url(r'^logout/?$', logout_view, name='logout'),
    url(r'^$', account_view, name='home'),
]
