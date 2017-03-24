from django.urls import reverse
from django.views.generic import DeleteView
from django.http import HttpResponseRedirect
from recipe.models import Recipe
from .models import Review, ReviewForm
from utils.utils import make_ownership_dispatch


def review_create_view(request, pk):
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse('auth_login'))
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.recipe = Recipe.objects.filter(pk=pk).first()
        review.save()
    return HttpResponseRedirect(reverse('view_recipe', args=[pk]))


class ReviewDeleteView(DeleteView):
    model = Review
    dispatch = make_ownership_dispatch(lambda: ReviewDeleteView)
    template_name = 'delete_review.html'

    def get_success_url(self):
        return reverse('view_recipe', args=[self.object.recipe.id])
