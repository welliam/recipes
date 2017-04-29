from django.views.generic import TemplateView
from django.contrib.auth.models import User


class ShoppingListDetailView(TemplateView):
    """View for viewing shopping lists."""
    model = User
    template_name = 'view_shopping_list.html'
