from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^session/', include('autostew_web_session.urls')),
    url(r'^admin/', admin.site.urls),
]
