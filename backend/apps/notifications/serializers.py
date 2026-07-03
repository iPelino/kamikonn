from rest_framework import serializers

from .models import NotificationPreference


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            "rsvp_confirmation",
            "event_reminder",
            "new_from_followed",
            "event_updates",
        ]
