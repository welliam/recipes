import re
from functools import reduce
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
     TemplateView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect, HttpResponseForbidden
from utils.utils import make_ownership_dispatch
from .models import Recipe
from review.models import ReviewForm


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
        recipebooks = self.object.user.recipebooks.all()
        context['recipebooks'] = zip(
            recipebooks,
            (self.object in book.recipes.all() for book in recipebooks)
        )
        context['review_form'] = ReviewForm
        context['request_user'] = self.request.user
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """View that creates a recipe."""
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
    dispatch = make_ownership_dispatch(lambda: RecipeUpdateView)


class RecipeDeleteView(DeleteView):
    """Delete recipe."""
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('home')
    dispatch = make_ownership_dispatch(lambda: RecipeDeleteView)


def update_recipebooks(request, pk):
    if request.method == 'POST':
        recipe = Recipe.objects.filter(pk=pk).first()
        if recipe.user != request.user:
            return HttpResponseForbidden()
        recipe.recipebooks.set(request.POST.getlist('books'))
    return HttpResponseRedirect(reverse('view_recipe', args=[pk]))
