from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.db import connection
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health_check(request):
    """Simple health check endpoint for deployment verification."""
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False
    return JsonResponse({"status": "ok", "db": db_ok})


urlpatterns = [
    path("admin/", admin.site.urls),
    # OpenAPI Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Health check
    path("api/health/", health_check, name="health-check"),
    # API endpoints
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.events.urls")),
    path("api/v1/organizers/", include("apps.organizers.urls")),
    path("api/v1/", include("apps.universities.urls")),
    path("api/v1/moderation/", include("apps.moderation.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
