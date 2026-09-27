# /home/urls.py (Your new app)

from django.urls import path, include
from . import views
from wagtail import urls as wagtail_urls

urlpatterns = [
    # If you have a simple 'index' view in home/views.py for testing
   #path('', views.portfolio_home, name='home_index'),
   #path("portfolio/", include(wagtail_urls)),
]