from django.views.generic.base import TemplateView

from autostew_web_contact.models import ContactMessage
from autostew_web_session.models.server import Server


class HomeView(TemplateView):
    template_name = 'autostew_web_home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['unread_messages'] = ContactMessage.objects.filter(read=False)
        context['unverified_servers'] = Server.objects.filter(back_verified=False)
        context['servers_in_race'] = [server for server in Server.objects.filter(current_session__isnull=False) if server.is_up]
        context['servers_online'] = [server for server in Server.objects.filter(current_session__isnull=True) if server.is_up]
        return context
