from django.conf.urls import url
from .views import (
    RecipeBookCreateView,
    RecipeBookDetailView,
    RecipeBookUpdateView
)

urlpatterns = [
    url(r'new$', RecipeBookCreateView.as_view(), name='new_recipebook'),
    url(r'(?P<pk>[0-9]+)$',
        RecipeBookDetailView.as_view(),
        name='view_recipebook'),
    url(r'(?P<pk>[0-9]+)/edit$',
        RecipeBookUpdateView.as_view(),
        name='edit_recipebook'),
]
