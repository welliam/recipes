from random import randint
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse


def create_unique_urlindex(lower_bound=100000000):
    """Creates a unique urlindex.

    Ensures the generated value is not already a urlindex."""
    while True:
        i = randint(lower_bound, lower_bound*10-1)
        if not Recipe.objects.filter(id=i).exists():
            return i


@python_2_unicode_compatible
class Recipe(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
        default=create_unique_urlindex
    )
    user = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    ingredients = models.TextField()
    directions = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Recipe {} "{}">'.format(self.id, self.title)

    def get_absolute_url(self):
        return reverse('view_recipe', args=[str(self.id)])

    def get_average_score(self):
        reviews_count = self.reviews.count()
        score_sum = sum(map(lambda r: r.score, self.reviews.all()))
        if reviews_count:
            return round(score_sum / reviews_count, 1)
