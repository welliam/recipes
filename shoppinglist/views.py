from django.views.generic import CreateView
from .models import ShoppingList


class ShoppingListCreateView(CreateView):
    """View for creating shopping lists."""
    model = ShoppingList
    template_name = 'create_shopping_list.html'
    fields = ['title']

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(ShoppingListCreateView, self).form_valid(form)
