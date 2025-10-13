from django.urls import path, include

from dashboard.views import home as dashboard_view



from .views import home


urlpatterns = [
    path("", dashboard_view, name="home"),
    #path("", home, name="home"),
    path('companies/', include('companies.urls')),
    path("products/", include("catalog.urls")),
    path("stocks/", include("inventory.urls")),
    path("alerts/", include("alerts.urls")),
    path("users/", include("users.urls")),
    path("dashboard/", include("dashboard.urls")),
    ]



