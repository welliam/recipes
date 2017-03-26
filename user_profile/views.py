from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.http import HttpResponseRedirect
from .models import UserProfile


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile_detail.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['recipes'] = self.object.recipes.all()[:5]
        context['own_profile'] = self.object == self.request.user
        context['recipebooks'] = self.object.recipebooks.all()[:5]
        context['follows'] = self.object.profile.follows.all()[:5]
        return context


class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'edit_profile.html'
    fields = ['bio']

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])


def follow_view(request, slug):
    """Add a follower."""
    user = User.objects.filter(username=slug).first()
    request.user.profile.follows.add(user)
    return HttpResponseRedirect(reverse('profile', args=[slug]))
