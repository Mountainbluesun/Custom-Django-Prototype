from django.urls import path, include
from django.conf import settings
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as documents_urls

from dashboard.views import home as dashboard_view, test_video

urlpatterns = [
    # ---------------------
    # Accueil de votre application
    # ---------------------
    path("", dashboard_view, name="home"),
    path('', include('portfolio.urls')),
    path('', include('core.urls')),
    path('captcha/', include('captcha.urls')),


    # ---------------------
    # Apps de votre projet
    # ---------------------
    path('companies/', include('companies.urls')),
    path('products/', include('catalog.urls')),
    path('stocks/', include('inventory.urls')),
    path('alerts/', include('alerts.urls')),
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
   # path("portfolio/", include("home.urls")),
    path('test-video/', test_video, name='test_video'),
    ]

if settings.DEBUG:
        from django.conf.urls.static import static
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        urlpatterns += staticfiles_urlpatterns()
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Wagtail Admin et CMS
    # ---------------------
urlpatterns += [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(documents_urls)),
    path("", include(wagtail_urls)),



    # Les pages Wagtail (toujours en dernier)
    # path("", include(wagtail_urls)),
    path("", include(wagtail_urls)),
]
