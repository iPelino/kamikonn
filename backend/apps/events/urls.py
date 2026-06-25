from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.events.views import CategoryViewSet, EventViewSet, ModerationEventViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"moderation/events", ModerationEventViewSet, basename="moderation-event")

urlpatterns = [
    path("", include(router.urls)),
]
