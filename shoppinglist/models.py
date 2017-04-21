from random import randint
from django.db import models
from django.contrib.auth.models import User


def create_unique_urlindex(lower_bound=100000000):
    """Creates a unique urlindex.

    Ensures the generated value is not already a urlindex."""
    while True:
        i = randint(lower_bound, lower_bound*10-1)
        if not ShoppingList.objects.filter(id=i).exists():
            return i


class ShoppingList(models.Model):
    """Model for user shopping lists."""
    id = models.PositiveIntegerField(
        primary_key=True,
        default=create_unique_urlindex
    )
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
