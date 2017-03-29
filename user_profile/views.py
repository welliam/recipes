from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.http import HttpResponseRedirect
from utils.utils import paginate
from .models import UserProfile


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile_detail.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context.update(paginate(
            self.request,
            self.object.recipes.order_by('-date_created')
        ))
        context['own_profile'] = self.object == self.request.user
        recipebooks = self.object.recipebooks
        context['recipebooks'] = recipebooks.order_by('-date_created')[:5]
        context['follows'] = self.object.profile.follows.all()[:5]
        if self.request.user.is_authenticated():
            context['followed'] = self.request.user.profile.follows.filter(
                username=self.object.username
            ).count()
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
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse('auth_login'))
    user = User.objects.filter(username=slug).first()
    if request.POST['follow'] == 'follow':
        request.user.profile.follows.add(user)
    else:
        request.user.profile.follows.remove(user)
    return HttpResponseRedirect(reverse('profile', args=[slug]))
