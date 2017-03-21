from django.conf.urls import url
from .views import RecipeBookCreateView

urlpatterns = [
    url('new$', RecipeBookCreateView.as_view(), name='new_recipebook')
]
