import re
from functools import reduce
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import (
     TemplateView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Recipe


def splitDirectionLine(direction):
    """Split a direction line into its summary and details."""
    try:
        t, d = direction.split('\n', 1)
    except ValueError:
        t, d = direction, ''
    return dict(summary=t.strip(), details=d.strip())


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
        context['ingredients'] = self.object.ingredients.split('\n')
        context['directions'] = structureDirections(self.object.directions)
        context['own_recipe'] = self.object.user == self.request.user
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


class RecipeSearchView(TemplateView):
    """View which renders search results."""
    template_name = "search_results.html"

    def get_context_data(self, **kwargs):
        context = super(RecipeSearchView, self).get_context_data(**kwargs)
        query = self.request.GET['q']
        context['recipes'] = reduce(
            lambda o, w: o.filter(title__contains=w),
            query.split()[:20],
            Recipe.objects.all()
        )
        context['query'] = query
        return context


class RecipeUpdateView(UpdateView):
    """Update recipe."""
    model = Recipe
    template_name = 'edit_recipe.html'
    fields = ['title', 'description', 'ingredients', 'directions']

    def dispatch(self, request, *args, **kwargs):
        """Check if the recipe to edit is owned by user."""
        pk = kwargs.get('pk')
        try:
            device = request.user.recipes.filter(pk=pk).first()
        except AttributeError:  # user not logged in
            return HttpResponseRedirect(reverse('auth_login'))
        if device:
            return super(RecipeUpdateView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden()


class RecipeDeleteView(DeleteView):
    """Delete recipe."""
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        """Check if the recipe to delete is owned by user."""
        pk = kwargs.get('pk')
        try:
            device = request.user.recipes.filter(pk=pk).first()
        except AttributeError:  # user not logged in
            return HttpResponseRedirect(reverse('auth_login'))
        if device:
            return super(RecipeDeleteView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponseForbidden()
