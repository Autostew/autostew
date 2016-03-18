from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^session/', include('autostew_web_session.urls')),
    url(r'^user/', include('autostew_web_users.urls')),
    url(r'^', TemplateView.as_view(template_name='autostew_web_session/home.html'), name='home'),
]
