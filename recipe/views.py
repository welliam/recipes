import re
from functools import reduce
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
     TemplateView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect, HttpResponseForbidden
from utils.utils import make_ownership_dispatch, paginate
from .models import Recipe, RecipeForm
from recipebook.models import RecipeBook
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
        if self.request.user.is_authenticated():
            recipebooks = self.request.user.recipebooks.all()
            context['recipebooks'] = zip(
                recipebooks,
                (self.object in book.recipes.all() for book in recipebooks)
            )
        context['review_form'] = ReviewForm
        context['reviews'] = self.object.reviews.order_by('-date_created')[:5]
        context['request_user'] = self.request.user
        context['recipe_form'] = RecipeForm(initial=self.object.__dict__)
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
            lambda o, w: o.filter(title__icontains=w),
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


def any_recipebooks_user_mismatched(user, book_pks):
    for pk in book_pks:
        book = RecipeBook.objects.filter(id=pk).first()
        if book and book.user != user:
            return True


def update_recipebooks(request, pk):
    if request.method == 'POST':
        books = request.POST.getlist('books')
        recipe = Recipe.objects.filter(pk=pk).first()
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('auth_login'))
        elif any_recipebooks_user_mismatched(request.user, books):
            return HttpResponseForbidden()
        recipe.recipebooks.set(books)
    return HttpResponseRedirect(reverse('view_recipe', args=[pk]))


class ReviewsListView(DetailView):
    """View that renders a recipe."""
    model = Recipe
    template_name = 'recipe_reviews.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewsListView, self).get_context_data(**kwargs)
        context.update(paginate(
            self.request,
            self.object.reviews.order_by('-date_created'))
        )
        return context
