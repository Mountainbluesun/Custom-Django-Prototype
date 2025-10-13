from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    path("", views.product_list, name="list"),
    path("create/", views.product_create, name="create"),
    path("<int:pid>/edit/", views.product_edit, name="edit"),
    path("<int:pid>/delete/", views.product_delete, name="delete"),
# CSV:
    path("import/", views.products_import_csv, name="import_csv"),
    path("export/", views.products_export_csv, name="export_csv"),
    path("import-page/", views.product_import_page_view, name="import_page"), # <-- Ajoutez cette ligne
]

















