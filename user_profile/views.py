from django.contrib.auth.models import User
from django.views.generic import DetailView


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile_detail.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['recipes'] = self.object.recipes.all()[:5]
        return context

