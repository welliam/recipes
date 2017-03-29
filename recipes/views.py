from itertools import chain
from django.views.generic.base import TemplateView
from utils.utils import paginate
from recipe.models import Recipe


def get_recipes(user):
    followed_recipes = chain.from_iterable(
        user.recipes.all()
        for user in user.profile.follows.all()
    )
    user_recipes = user.recipes.all()
    return chain(followed_recipes, user_recipes)


class HomePage(TemplateView):
    """View for the home page."""
    template_name = 'recipes/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            recipes = list(get_recipes(self.request.user))
            if not recipes:
                recipes = Recipe.objects.all()
                context['no_recipes'] = True
        else:
            recipes = Recipe.objects.all()
        sorted_recipes = sorted(
            recipes,
            key=lambda r: r.date_created, reverse=True
        )
        context.update(paginate(self.request, sorted_recipes))
        return context


class AboutPage(TemplateView):
    """View for the about page."""
    template_name = 'recipes/about.html'
