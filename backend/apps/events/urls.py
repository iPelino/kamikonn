from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.events.rsvp_views import RSVPViewSet, SavedEventViewSet
from apps.events.views import CategoryViewSet, EventViewSet, ModerationEventViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"moderation/events", ModerationEventViewSet, basename="moderation-event")

# Nested routers for per-event RSVP and Save actions.
# These produce URLs like: /events/{event_slug}/rsvp/ and /events/{event_slug}/save/
rsvp_router = DefaultRouter()
rsvp_router.register(r"", RSVPViewSet, basename="event-rsvp")

save_router = DefaultRouter()
save_router.register(r"", SavedEventViewSet, basename="event-save")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "events/<str:event_slug>/",
        include(
            [
                path("", include(rsvp_router.urls)),
                path("", include(save_router.urls)),
            ]
        ),
    ),
]
