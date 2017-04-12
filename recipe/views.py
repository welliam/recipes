import re
from functools import reduce
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
     TemplateView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect, HttpResponseForbidden
from utils.utils import paginate, ownership_dispatch
from .models import Recipe, RecipeForm
from recipebook.models import RecipeBook, RecipeBookForm
from review.models import ReviewForm
from notification.models import Notification


class RecipeDetailView(DetailView):
    """View that renders a recipe."""
    model = Recipe
    template_name = 'view_recipe.html'

    def get_context_data(self, **kwargs):
        """Attach necessary context."""
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
        context['derive_form'] = RecipeForm(initial=self.object.__dict__)
        context['review_form'] = ReviewForm
        context['reviews'] = self.object.reviews.order_by('-date_created')[:5]
        context['request_user'] = self.request.user
        context['recipe_form'] = RecipeForm(initial=self.object.__dict__)
        context['recipebook_form'] = RecipeBookForm
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """View that creates a recipe."""
    model = Recipe
    template_name = 'create_recipe.html'
    fields = ['title', 'description', 'ingredients', 'directions']

    def form_valid(self, form):
        """Attach user and origin_recipe (if supplied) to form.

        Send notification for derived recipe."""
        form.instance.user = self.request.user
        id = self.request.POST.get('origin_recipe')
        origin_recipe = Recipe.objects.filter(id=id).first()
        if origin_recipe:
            form.instance.origin_recipe = origin_recipe
            Notification(
                user=origin_recipe.user,
                type='derive',
                object_key=form.instance.id
            ).save()
        return super(RecipeCreateView, self).form_valid(form)


class RecipeSearchView(TemplateView):
    """View for rendering search results."""
    template_name = "search_results.html"

    def get_context_data(self, **kwargs):
        """Process and find matching objects for the query."""
        context = super(RecipeSearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        cleaned = [w for w in query.split() if w[2:]]
        if cleaned:
            search_results = reduce(
                lambda o, w: o.filter(title__icontains=w),
                cleaned,
                Recipe.objects.all()
            )
            context.update(paginate(self.request, search_results))
        context['query'] = query
        return context


@ownership_dispatch
class RecipeUpdateView(UpdateView):
    """View for updating recipe."""
    model = Recipe
    template_name = 'edit_recipe.html'
    fields = ['title', 'description', 'ingredients', 'directions']


@ownership_dispatch
class RecipeDeleteView(DeleteView):
    """Delete recipe."""
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('home')


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


class DeriveRecipeView(LoginRequiredMixin, TemplateView):
    template_name = 'derive_recipe.html'

    def get_context_data(self, **kwargs):
        context = super(DeriveRecipeView, self).get_context_data(**kwargs)
        recipe = Recipe.objects.filter(pk=self.kwargs['pk']).first()
        context['object'] = recipe
        context['form'] = RecipeForm(initial=recipe.__dict__)
        return context


class DerivedRecipesListView(DetailView):
    """View that lists derived recipes."""
    model = Recipe
    template_name = 'derived_recipes.html'

    def get_context_data(self, **kwargs):
        """Attach derivations of recipe to context."""
        context = super(
            DerivedRecipesListView, self
        ).get_context_data(**kwargs)
        context.update(paginate(
            self.request,
            self.object.recipe_derivations.order_by('-date_created'))
        )
        return context


def update_recipebooks_view(request, pk):
    """View for updating recipebooks contain a recipe.

    For POST requests only. To be used internally for AJAX
    requests."""
    if request.method == 'POST':
        books = request.POST.getlist('books')
        recipe = Recipe.objects.filter(pk=pk).first()
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('auth_login'))
        elif any_recipebooks_user_mismatched(request.user, books):
            return HttpResponseForbidden()
        recipe.recipebooks.set(books)
    return HttpResponseRedirect(reverse('view_recipe', args=[pk]))


def any_recipebooks_user_mismatched(user, book_pks):
    """Check if recipebooks are all owned by user."""
    for pk in book_pks:
        book = RecipeBook.objects.filter(id=pk).first()
        if book and book.user != user:
            return True


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
