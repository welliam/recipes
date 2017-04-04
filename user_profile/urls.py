from django.conf.urls import url
from .views import (
    ProfileDetailView,
    RecipeBooksListView,
    ProfileUpdateView,
    follow_view,
    FollowingListView,
    FollowersListView,
)

urlpatterns = [
    url(r'p/(?P<slug>\w+)$', ProfileDetailView.as_view(), name='profile'),
    url(r'p/(?P<slug>\w+)/following$',
        FollowingListView.as_view(),
        name='following_list'),
    url(r'p/(?P<slug>\w+)/followers$',
        FollowersListView.as_view(),
        name='followers_list'),
    url('recipebooks/(?P<slug>\w+)',
        RecipeBooksListView.as_view(),
        name='profile_recipebooks'),
    url('edit$', ProfileUpdateView.as_view(), name='edit_profile'),
    url('follow/(?P<slug>\w+)$', follow_view, name='follow'),
]
