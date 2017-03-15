from django.conf.urls import url
from .views import ProfileDetailView


urlpatterns = [
    url(r'^$', ProfileDetailView.as_view(), name='profile')
]
