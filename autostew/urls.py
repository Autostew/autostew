from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^session/', include('autostew_web_session.urls'), name='session'),
    url(r'^user/', include('autostew_web_users.urls'), name='user'),
    url(r'^', include('autostew_web_home.urls'), name='home'),
]
