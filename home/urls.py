# /home/urls.py (Votre nouvelle application)

from django.urls import path, include
from . import views
from wagtail import urls as wagtail_urls

urlpatterns = [
    # Si vous avez une vue 'index' simple dans home/views.py pour tester
   #path('', views.portfolio_home, name='home_index'),
   #path("portfolio/", include(wagtail_urls)),
]