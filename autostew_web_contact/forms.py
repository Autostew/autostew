from django.forms import ModelForm
from autostew_web_contact.models import ContactMessage


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
