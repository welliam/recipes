from django.conf.urls import url
from .views import ProfileDetailView, ProfileUpdateView, follow_view


urlpatterns = [
    url(r'p/(?P<slug>\w+)$', ProfileDetailView.as_view(), name='profile'),
    url('edit$', ProfileUpdateView.as_view(), name='edit_profile'),
    url('follow/(?P<slug>\w+)$', follow_view, name='follow'),
]
