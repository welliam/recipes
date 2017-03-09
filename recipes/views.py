from django.views.generic.base import TemplateView

class HomePage(TemplateView):
    """View for the home page."""
    template_name = 'recipes/home.html'
