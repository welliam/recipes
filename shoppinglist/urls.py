from django.conf.urls import url
from .views import ShoppingListDetailView

urlpatterns = [
    url(r'$', ShoppingListDetailView.as_view(), name='view_shopping_list'),
]
