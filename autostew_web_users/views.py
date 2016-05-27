import sys
from django.views import generic

from autostew_web_users.models import SteamUser


class SteamUserListView(generic.ListView):
    model = SteamUser

    def get_queryset(self):

        sys.stderr.write('\nin get_queryset' + '\n')

        name = self.request.GET.get("name")
        if name is not None and name != '':
            exact_search = self.model.objects.filter(display_name__exact=name)
            contains_search = self.model.objects.filter(display_name__icontains=name)
            if len(exact_search) == 1:
                object_list = self.center_around_user_searched_for(exact_search[0])
            elif len(contains_search) == 1:
                object_list = self.center_around_user_searched_for(contains_search[0])
            else:
                object_list = self.model.objects.filter(display_name__icontains=name)
        else:
            object_list = self.model.objects.all()
        return object_list

    def center_around_user_searched_for(self, user_searched_for, result_length=50):
        all_users = self.model.objects.all()
        l = list(all_users)  # automatically ordered by elo_rating
        index = l.index(user_searched_for)
        lower_index = index-(result_length / 2) if index-(result_length / 2) >= 0 else 0
        upper_index = index+(result_length / 2) if index+(result_length / 2) < len(l) else len(l)-1
        object_list = self.model.objects.all()[lower_index:upper_index]
        return object_list

    def get_context_data(self, **kwargs):
        sys.stderr.write('\n in get_context_data' + '\n')
        context = super(SteamUserListView, self).get_context_data(**kwargs)
        context['page'] = self.request.GET.get('page', '1')
        return context
