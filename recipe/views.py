import re
from django.views.generic import DetailView, CreateView
from .models import Recipe


def splitDirectionLine(direction):
    """Split a direction line into its summary and details."""
    try:
        t, d = direction.split('\n', 1)
    except ValueError:
        t, d = direction, ''
    return dict(title=t.strip(), direction=d.strip())


def removeNewlineWhitespace(s):
    """Remove whitespace surrounding newlines.

    Also remove \rs."""
    return re.sub('[ \t]*\n[ \t]*', '\n', re.sub('\r', '', s))


def structureDirections(directions):
    """Structure directions.

    Directions are entered like:
    <direction summary>\n<direction details>...
    """
    directionLines = removeNewlineWhitespace(directions).split('\n\n')
    return map(splitDirectionLine, directionLines)


class RecipeDetailView(DetailView):
    """View that renders a recipe."""
    model = Recipe
    template_name = 'view_recipe.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        self.object.ingredients = self.object.ingredients.split('\n')
        self.object.directions = structureDirections(self.object.directions)
        return context


class RecipeCreateView(CreateView):
    """View that renders a recipe."""
    model = Recipe
    template_name = 'create_recipe.html'
    fields = ['title', 'description', 'ingredients', 'directions']

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(RecipeCreateView, self).form_valid(form)
