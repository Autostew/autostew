import logging

from django.forms import ModelForm

from autostew_web_session.models.session import SessionSetup
from autostew_web_session.models.server import Server


class SessionSetupForm(ModelForm):
    def save(self, commit=True):
        session_setup = super(SessionSetupForm, self).save(commit=False)
        session_setup.is_template = True
        if commit:
            session_setup.save()

        return session_setup

    class Meta:
        exclude = ['is_template']
        model = SessionSetup
