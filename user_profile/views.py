from django.contrib.auth.models import User
from django.views.generic import DetailView


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile_detail.html'
    slug_field = 'username'
