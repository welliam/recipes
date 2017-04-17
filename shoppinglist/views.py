from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ShoppingList


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    """View for creating shopping lists."""
    model = ShoppingList
    template_name = 'create_shopping_list.html'
    fields = ['title']

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(ShoppingListCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])
