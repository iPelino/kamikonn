from django.urls import path

from .views import BecomeOrganizerView, CurrentOrganizerProfileView, OrganizerProfileDetailView

app_name = "organizers"

urlpatterns = [
    path("become/", BecomeOrganizerView.as_view(), name="become_organizer"),
    path("me/", CurrentOrganizerProfileView.as_view(), name="current_organizer"),
    path("<int:user_id>/", OrganizerProfileDetailView.as_view(), name="organizer_detail"),
]
