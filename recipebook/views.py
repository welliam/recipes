from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
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
        return reverse('profile', args=[self.request.user.username])


class RecipeBookDetailView(DetailView):
    model = RecipeBook
    template_name = 'view_recipebook.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeBookDetailView, self).get_context_data(**kwargs)
        context['recipes'] = self.object.recipes.all()[:5]
        return context


class RecipeBookUpdateView(UpdateView):
    model = RecipeBook
    template_name = 'edit_recipebook.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(RecipeBookUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])
