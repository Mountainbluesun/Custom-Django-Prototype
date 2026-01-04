from django.urls import path
from .views import laravel_project

urlpatterns = [
    path('projets/laravel/', laravel_project, name='laravel_project'),
]
