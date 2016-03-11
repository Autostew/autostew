from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^', include('autostew_web_session.urls')),
]
