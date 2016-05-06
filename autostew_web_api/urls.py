from django.conf.urls import include, url
from rest_framework import routers

from autostew_web_api import views


router = routers.DefaultRouter()
router.register(r'sessions', views.SessionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]