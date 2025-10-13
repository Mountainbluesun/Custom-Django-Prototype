from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
    path("", views.company_list, name="list"),
    path("create/", views.company_create, name="create"),
    path("<int:company_id>/edit/", views.company_edit, name="edit"),
    path("<int:company_id>/delete/", views.company_delete, name="delete"),


]
