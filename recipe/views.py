from django.views.generic import DetailView, CreateView
from .models import Recipe


class RecipeDetailView(DetailView):
    """View that renders a recipe."""
    model = Recipe
    template_name = 'view_recipe.html'


class RecipeCreateView(CreateView):
    """View that renders a recipe."""
    model = Recipe
    template_name = 'create_recipe.html'
    fields = ['title', 'description', 'ingredients', 'directions']

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(RecipeCreateView, self).form_valid(form)
