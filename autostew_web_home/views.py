from django.views.generic.base import TemplateView

from autostew_web_contact.models import ContactMessage


class HomeView(TemplateView):
    template_name = 'autostew_web_home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['unread_messages'] = ContactMessage.objects.filter(read=False)
        return context
