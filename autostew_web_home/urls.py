from django.conf.urls import url

from autostew_web_home.views import HomeView

urlpatterns = [
    url(r'^', HomeView.as_view(), name='home'),
]
