from django.conf.urls import url
from .views import notifications_view

urlpatterns = [
    url(r'$', notifications_view, name='view_notifications'),
]
