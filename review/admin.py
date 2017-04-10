from django.contrib import admin
from .models import Review


@admin.register(Review)
class RecipeBookAdmin(admin.ModelAdmin):
    pass
