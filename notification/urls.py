from django.conf.urls import url
from .views import notifications_view, notification_count_view

urlpatterns = [
    url(r'/$', notifications_view, name='view_notifications'),
    url(r'/count$', notification_count_view, name='notification_count_view'),
]
