from django.conf.urls import url
from .views import RecipeDetailView

urlpatterns = [
    url(r'(?P<pk>[0-9]+)$', RecipeDetailView.as_view(), name='view_recipe')
]
