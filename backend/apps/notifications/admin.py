from django.contrib import admin

from .models import NotificationPreference


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "rsvp_confirmation",
        "event_reminder",
        "new_from_followed",
        "event_updates",
    )
    list_filter = ("rsvp_confirmation", "event_reminder")
