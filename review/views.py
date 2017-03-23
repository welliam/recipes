from django.urls import reverse
from django.http import HttpResponseRedirect
from recipe.models import Recipe
from .models import ReviewForm


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
