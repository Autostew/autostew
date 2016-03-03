from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^session/', include('autostew_web_session.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^tracks/', include('autostew_web_session.urls')),
]
