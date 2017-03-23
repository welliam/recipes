from django.views.generic import CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from recipe.models import Recipe
from .models import Review


def review_create_view(request, pk):
    recipe = Recipe.objects.filter(pk=pk).first()
    Review(
        user=request.user,
        recipe=recipe,
        title=request.POST['title'],
        body=request.POST['body'],
        score=request.POST['score']
    ).save()
    return HttpResponseRedirect(reverse('view_recipe', args=[pk]))
