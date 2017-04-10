from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class RecipeBookAdmin(admin.ModelAdmin):
    pass
