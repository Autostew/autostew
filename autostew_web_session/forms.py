import logging

from django.forms import ModelForm

from autostew_web_session.models import SessionSetup, Server


class SessionSetupForm(ModelForm):
    def save(self, commit=True):
        session_setup = super(SessionSetupForm, self).save(commit=False)
        if commit:
            session_setup.save()
            logging.info("Saving new session setup %s" % session_setup.name)

        # TODO: Choose the server to add this setup to in the form and only add the new config to that server
        for server in Server.objects.all():
            server.session_setups.add(session_setup)

        return session_setup

    class Meta:
        exclude = []
        model = SessionSetup
