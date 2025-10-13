from django.urls import path
from .views import alerts_list
from . import views

app_name = 'alerts'

urlpatterns = [
    path("", alerts_list, name="alerts_list"),
    path("", views.alerts_list, name="list"),
]
