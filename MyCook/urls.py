from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from MyCook import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Recipes.web_urls')),
    path('api/', include('Recipes.api_urls'))
]


if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)