from django.contrib.auth.models import User
from django.views.generic import DetailView


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile_detail.html'

    def get_object(self):
        """Return the user's profile."""
        return self.request.user
