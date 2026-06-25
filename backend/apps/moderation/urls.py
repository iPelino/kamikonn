from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.moderation.views import FlagReportViewSet, ModerationLogViewSet

app_name = "moderation"

router = DefaultRouter()
router.register(r"flags", FlagReportViewSet, basename="flag")
router.register(r"logs", ModerationLogViewSet, basename="log")

urlpatterns = [
    path("", include(router.urls)),
]
