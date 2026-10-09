from django.urls import path, include
from django.conf import settings
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as documents_urls

from dashboard.views import home as dashboard_view, test_video

urlpatterns = [
    # ---------------------
    # Your application's home screen
    # ---------------------
    path("", dashboard_view, name="home"),
    path('', include('portfolio.urls')),
    path('', include('core.urls')),
    path('captcha/', include('captcha.urls')),


    # ---------------------
    # Your project's apps
    # ---------------------
    path('companies/', include('companies.urls')),
    path('products/', include('catalog.urls')),
    path('stocks/', include('inventory.urls')),
    path('alerts/', include('alerts.urls')),
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('test-video/', test_video, name='test_video'),
    ]

if settings.DEBUG:
        from django.conf.urls.static import static
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        urlpatterns += staticfiles_urlpatterns()
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Wagtail Admin and CMS
    # ---------------------
urlpatterns += [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(documents_urls)),
    path("", include(wagtail_urls)),
]
