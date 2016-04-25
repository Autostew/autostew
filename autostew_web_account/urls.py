from django.conf.urls import url

from autostew_web_account.views import login_view, account_view, logout_view, register_view

urlpatterns = [
    url(r'^edit_server', register_view, name='edit_server'),
    url(r'^register', register_view, name='register'),
    url(r'^login', login_view, name='login'),
    url(r'^logout', logout_view, name='logout'),
    url(r'^', account_view, name='home'),
]
