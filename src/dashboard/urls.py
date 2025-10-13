# src/dashboard/urls.py
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),      # /dashboard/
    #path("view/", views.dashboard_view, name="view"), # /dashboard/view/
]
