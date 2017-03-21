from django.conf.urls import url
from .views import ProfileDetailView, ProfileUpdateView


urlpatterns = [
    url(r'p/(?P<slug>\w+)$', ProfileDetailView.as_view(), name='profile'),
    url('edit$', ProfileUpdateView.as_view(), name='edit_profile'),
]
