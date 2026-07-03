from django.urls import path

from .views import NotificationPreferenceView

urlpatterns = [
    path("preferences/", NotificationPreferenceView.as_view(), name="notification-preferences"),
]
