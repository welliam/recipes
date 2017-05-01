from django.db import models
from django.contrib.auth.models import User


class ShoppingListItem(models.Model):
    """Model for shopping list items."""
    user = models.ForeignKey(
        User,
        related_name='shopping_list_items',
        on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=50)
    done = models.BooleanField(default=False)
