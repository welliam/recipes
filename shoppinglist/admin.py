from django.contrib import admin
from .models import ShoppingList, ShoppingListItem


@admin.register(ShoppingList)
@admin.register(ShoppingListItem)
class ShoppingListAdmin(admin.ModelAdmin):
    pass
