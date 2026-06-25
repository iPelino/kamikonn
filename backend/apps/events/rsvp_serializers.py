from rest_framework import serializers

from apps.events.models import RSVP, SavedEvent


class RSVPSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    event_title = serializers.ReadOnlyField(source="event.title")
    event_slug = serializers.ReadOnlyField(source="event.slug")

    class Meta:
        model = RSVP
        fields = [
            "id",
            "event",
            "event_title",
            "event_slug",
            "user",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]


class SavedEventSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    event_title = serializers.ReadOnlyField(source="event.title")
    event_slug = serializers.ReadOnlyField(source="event.slug")

    class Meta:
        model = SavedEvent
        fields = [
            "id",
            "event",
            "event_title",
            "event_slug",
            "user",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
