
from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.stock_list, name="list"),
    path('in/', views.stock_in, name='stock_in'),
    path("in/", views.stock_in, name="in"),
    path("out/", views.stock_out, name="out"),
    path('out/', views.stock_out, name='stock_out'),
    path("transfer/", views.stock_transfer, name="transfer"),
    #path("alerts/", views.alerts, name="alerts"),


]
