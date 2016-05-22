from django.views import generic

from autostew_web_users.models import SteamUser


class SteamUserListView(generic.ListView):
    model = SteamUser

    def get_context_data(self, **kwargs):
        context = super(SteamUserListView, self).get_context_data(**kwargs)
        context['page'] = self.request.GET.get('page', '1')
        return context
