from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.events.views import CategoryViewSet, EventViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]
