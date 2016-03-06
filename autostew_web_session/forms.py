from django.forms import ModelForm

from autostew_web_session.models import SessionSetup


class SessionSetupForm(ModelForm):

    class Meta:
        exclude = []
        model = SessionSetup
