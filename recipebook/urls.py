from django.conf.urls import url
from .views import (
    RecipeBookCreateView,
    RecipeBookDetailView,
    RecipeBookUpdateView,
    RecipeBookDeleteView
)

urlpatterns = [
    url(r'new$', RecipeBookCreateView.as_view(), name='new_recipebook'),
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
