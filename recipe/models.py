from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse


@python_2_unicode_compatible
class Recipe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    ingredients = models.TextField()
    directions = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __repr__(self):
        return '<Recipe "{}">'.format(self.title)

    def get_absolute_url(self):
        return reverse('view_recipe', args=[str(self.id)])
