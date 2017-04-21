from django.conf.urls import url
from .views import ShoppingListCreateView, ShoppingListDetailView

urlpatterns = [
    url(r'(?P<pk>[0-9]+)$',
        ShoppingListDetailView.as_view(),
        name='view_shopping_list'),
    url(r'new$',
        ShoppingListCreateView.as_view(),
        name='create_shopping_list')
]
