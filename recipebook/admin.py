from django.contrib import admin

from .models import RecipeBook


@admin.register(RecipeBook)
class RecipeBookAdmin(admin.ModelAdmin):
    pass
