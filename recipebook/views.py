from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.utils import paginate, make_ownership_dispatch
from .models import RecipeBook


class RecipeBookCreateView(LoginRequiredMixin, CreateView):
    """View that creates a recipe."""
    model = RecipeBook
    template_name = 'create_recipebook.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(RecipeBookCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile_recipebooks', args=[self.request.user.username])


class RecipeBookDetailView(DetailView):
    model = RecipeBook
    template_name = 'view_recipebook.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeBookDetailView, self).get_context_data(**kwargs)
        context.update(paginate(self.request, self.object.recipes.all()))
        context['own_recipebook'] = self.object.user == self.request.user
        return context


class RecipeBookUpdateView(UpdateView):
    model = RecipeBook
    template_name = 'edit_recipebook.html'
    fields = ['title', 'description']
    dispatch = make_ownership_dispatch(lambda: RecipeBookUpdateView)


class RecipeBookDeleteView(DeleteView):
    model = RecipeBook
    template_name = 'delete_recipebook.html'
    dispatch = make_ownership_dispatch(lambda: RecipeBookDeleteView)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])
