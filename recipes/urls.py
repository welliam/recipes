from django.conf.urls import url, include
from django.contrib import admin
from .views import HomePage, AboutPage

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^about/', AboutPage.as_view(), name='about'),
    url(r'^profile/', include('user_profile.urls')),
    url(r'^recipe/', include('recipe.urls')),
    url(r'^recipebook/', include('recipebook.urls')),
    url(r'^review/', include('review.urls')),
    url(r'^notifications/', include('notification.urls')),
]
