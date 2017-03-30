from django.conf.urls import url
from .views import (
    RecipeBookCreateView,
    RecipeBookDetailView,
    RecipeBookUpdateView,
    RecipeBookDeleteView,
    recipe_book_ajax_create_view
)

urlpatterns = [
    url(r'new$', RecipeBookCreateView.as_view(), name='new_recipebook'),
    url(r'new_ajax$',
        recipe_book_ajax_create_view,
        name='ajax_create_recipebook'),
    url(r'(?P<pk>[0-9]+)$',
        RecipeBookDetailView.as_view(),
        name='view_recipebook'),
    url(r'(?P<pk>[0-9]+)/edit$',
        RecipeBookUpdateView.as_view(),
        name='edit_recipebook'),
    url(r'(?P<pk>[0-9]+)/delete$',
        RecipeBookDeleteView.as_view(),
        name='delete_recipebook'),
]
