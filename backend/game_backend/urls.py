from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("api/v1/accounts/", include("accounts.urls", namespace="accounts")),
    path("api/v1/games/", include("game.urls", namespace="game")),
    path("admin/", admin.site.urls),

    # Swagger/OpenAPI documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Serve React app for all non-API routes
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='react-app'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
