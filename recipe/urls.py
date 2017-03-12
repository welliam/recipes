from django.conf.urls import url
from .views import RecipeDetailView, RecipeCreateView

urlpatterns = [
    url(r'(?P<pk>[0-9]+)$', RecipeDetailView.as_view(), name='view_recipe'),
    url(r'new$', RecipeCreateView.as_view(), name='create_recipe'),
]
