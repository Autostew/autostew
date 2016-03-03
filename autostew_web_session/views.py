from django.views import generic

from .models import Track


class DetailView(generic.DetailView):
    model = Track
    template_name = 'autostew_web_session/track.html'

    def get_queryset(self):
        return Track.objects
