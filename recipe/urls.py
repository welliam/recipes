from django.conf.urls import url
from .views import (
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    RecipeSearchView,
    update_recipebooks,
    ReviewsListView,
)

urlpatterns = [
    url(r'new$', RecipeCreateView.as_view(), name='new_recipe'),
    url(r'(?P<pk>[0-9]+)$', RecipeDetailView.as_view(), name='view_recipe'),
    url(r'(?P<pk>[0-9]+)/edit$',
        RecipeUpdateView.as_view(),
        name='edit_recipe'),
    url(r'(?P<pk>[0-9]+)/delete$',
        RecipeDeleteView.as_view(),
        name='delete_recipe'),
    url(r'search', RecipeSearchView.as_view(), name='recipe_search'),
    url(r'(?P<pk>[0-9]+)/update_recipebooks',
        update_recipebooks,
        name='recipe_update_recipebooks'),
    url(r'(?P<pk>[0-9]+)/reviews$',
        ReviewsListView.as_view(),
        name='recipe_reviews'),
]
