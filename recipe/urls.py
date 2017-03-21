from django.conf.urls import url
from .views import (
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeSearchView,
)

urlpatterns = [
    url(r'new$', RecipeCreateView.as_view(), name='new_recipe'),
    url(r'(?P<pk>[0-9]+)$', RecipeDetailView.as_view(), name='view_recipe'),
    url(r'(?P<pk>[0-9]+)/edit$',
        RecipeUpdateView.as_view(),
        name='edit_recipe'),
    url(r'search', RecipeSearchView.as_view(), name='recipe_search'),
]
