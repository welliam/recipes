from django.conf.urls import url
from .views import ShoppingListCreateView

urlpatterns = [
    url(r'new$', ShoppingListCreateView.as_view(), name='create_shopping_list')
]
