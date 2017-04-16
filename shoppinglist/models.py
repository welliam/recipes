from django.db import models
from django.contrib.auth.models import User


class ShoppingList(models.Model):
    """Model for user shopping lists."""
    user = models.ForeignKey(
        User,
        related_name='shoppinglists',
        on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)


class ShoppingListItem(models.Model):
    """Model for shopping list items."""
    shoppinglist = models.ForeignKey(
        ShoppingList,
        related_name='items',
        on_delete=models.deletion.CASCADE
    )
    title = models.CharField(max_length=50)
    done = models.BooleanField()
