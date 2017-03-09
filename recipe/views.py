from django.shortcuts import render
from django.views.generic import DetailView
from .models import Recipe


class RecipeDetailView(DetailView):
    """View that renders a recipe."""
    model = Recipe
    template_name = 'view_recipe.html'
