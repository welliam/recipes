from django.views.generic.base import TemplateView
from recipe.models import Recipe


class HomePage(TemplateView):
    """View for the home page."""
    template_name = 'recipes/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.order_by('-date_created')[:5]
        return context


class AboutPage(TemplateView):
    """View for the about page."""
    template_name = 'recipes/about.html'
