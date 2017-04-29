from django.contrib import admin
from .models import ShoppingListItem


@admin.register(ShoppingListItem)
class ShoppingListAdmin(admin.ModelAdmin):
    pass
