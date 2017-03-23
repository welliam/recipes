from django.conf.urls import url
from .views import review_create_view

urlpatterns = [
    url('new/(?P<pk>[0-9]+)', review_create_view, name='new_review')
]
