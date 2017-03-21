from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from .models import UserProfile


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile_detail.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['recipes'] = self.object.recipes.all()[:5]
        return context


class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'edit_recipe.html'
    fields = ['bio']

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])
