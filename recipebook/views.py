from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.utils import paginate, ownership_dispatch
from .models import RecipeBook, RecipeBookForm


class RecipeBookCreateView(LoginRequiredMixin, CreateView):
    """View that creates a recipe."""
    model = RecipeBook
    template_name = 'create_recipebook.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        """Attach user to form."""
        form.instance.user = self.request.user
        return super(RecipeBookCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'profile_recipebooks',
            args=[self.request.user.username]
        )


class RecipeBookDetailView(DetailView):
    model = RecipeBook
    template_name = 'view_recipebook.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeBookDetailView, self).get_context_data(**kwargs)
        context.update(paginate(self.request, self.object.recipes.all()))
        context['own_recipebook'] = self.object.user == self.request.user
        context['recipebook_form'] = RecipeBookForm
        return context


@ownership_dispatch
class RecipeBookUpdateView(UpdateView):
    model = RecipeBook
    template_name = 'edit_recipebook.html'
    fields = ['title', 'description']


@ownership_dispatch
class RecipeBookDeleteView(DeleteView):
    model = RecipeBook
    template_name = 'delete_recipebook.html'

    def get_success_url(self):
        return reverse('profile_recipebooks', args=[self.request.user.username])


def recipe_book_ajax_create_view(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse('auth_login'))
    form = RecipeBookForm(request.POST)
    if form.is_valid():
        recipebook = form.save(commit=False)
        recipebook.user = request.user
        recipebook.save()
        return JsonResponse({'id': str(recipebook.id)})
