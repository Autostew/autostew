from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^accounts/', include('autostew_web_account.urls', namespace='account'), name='account'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^api/', include('autostew_web_api.urls', namespace='api'), name='api'),
    url(r'^contact/', include('autostew_web_contact.urls', namespace='contact'), name='contact'),
    url(r'^session/', include('autostew_web_session.urls', namespace='session'), name='session'),
    url(r'^user/', include('autostew_web_users.urls', namespace='users'), name='user'),
    url(r'^', include('autostew_web_home.urls', namespace='home'), name='home'),
]
