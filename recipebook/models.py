from random import randint
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from recipe.models import Recipe


def create_unique_urlindex(lower_bound=100000000):
    """Creates a unique urlindex.

    Ensures the generated value is not already a urlindex."""
    while True:
        i = randint(lower_bound, lower_bound*10-1)
        if not Recipe.objects.filter(id=i).exists():
            return i


class RecipeBook(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
        default=create_unique_urlindex
    )
    user = models.ForeignKey(
        User,
        related_name='recipebooks',
        on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    recipes = models.ManyToManyField(
        Recipe,
        related_name='recipebooks'
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('view_recipebook', args=[str(self.id)])


class RecipeBookForm(ModelForm):
    class Meta:
        model = RecipeBook
        fields = ['title', 'description']
