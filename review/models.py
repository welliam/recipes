from django.db import models
from django.contrib.auth.models import User
from recipe.models import Recipe


class Review(models.Model):
    user = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.deletion.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='reviews',
        on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=5000)
    score = models.PositiveSmallIntegerField(choices=((r,r) for r in range(1,6)))