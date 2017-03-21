from django.views.generic import CreateView
from django.urls import reverse
from .models import RecipeBook


class RecipeBookCreateView(CreateView):
    """View that creates a recipe."""
    model = RecipeBook
    template_name = 'create_recipe.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(RecipeBookCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])
