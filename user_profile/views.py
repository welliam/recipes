from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.http import HttpResponseRedirect
from utils.utils import paginate
from .models import UserProfile
from recipebook.models import RecipeBookForm
from notification.models import Notification


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
        context['follower_count'] = get_followers(self.object).count()
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
        Notification(
            user=user,
            type='follow',
            object_key=request.user.id
        ).save()
    else:
        request.user.profile.follows.remove(user)
    return HttpResponseRedirect(reverse('profile', args=[slug]))


class RecipeBooksListView(DetailView):
    model = User
    template_name = 'profile_recipebooks.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(RecipeBooksListView, self).get_context_data(**kwargs)
        context['own_profile'] = self.object == self.request.user
        context.update(paginate(
            self.request,
            self.object.recipebooks.order_by('-date_created')
        ))
        context['recipebook_form'] = RecipeBookForm
        return context


class FollowingListView(DetailView):
    model = User
    template_name = 'following_list.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(FollowingListView, self).get_context_data(**kwargs)
        context['following_list'] = True
        context.update(paginate(
            self.request,
            self.object.profile.follows.all()
        ))
        return context


class FollowersListView(DetailView):
    model = User
    template_name = 'following_list.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(FollowersListView, self).get_context_data(**kwargs)
        context.update(paginate(self.request, get_followers(self.object)))
        return context


def get_followers(user):
    return User.objects.filter(profile__follows__username=user.username)
