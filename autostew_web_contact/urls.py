from django.conf.urls import url

from autostew_web_contact.views import ContactFormView

urlpatterns = [
    url(r'^', ContactFormView.as_view(), name='contact'),
]
