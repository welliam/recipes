from django.conf.urls import url
from .views import ReviewDeleteView, review_create_view

urlpatterns = [
    url('new/(?P<pk>[0-9]+)', review_create_view, name='new_review'),
    url('delete/(?P<pk>[0-9]+)',
        ReviewDeleteView.as_view(),
        name='delete_review')
]
