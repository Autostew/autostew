
from django.views import generic

from .models import Track


class IndexView(generic.ListView):
    template_name = 'autostew_web_session/tracks.html'
    context_object_name = 'track_list'

    def get_queryset(self):
        return Track.objects.all().order_by('name')


class DetailView(generic.DetailView):
    model = Track
    template_name = 'autostew_web_session/track.html'
