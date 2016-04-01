from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from autostew_web_contact.forms import ContactForm


class ContactFormView(FormView):
    template_name = 'autostew_web_contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Thank you for your feedback! We will contact you soon if you provided an e-mail address."
        )
        return super(ContactFormView, self).form_valid(form)