from rest_framework import serializers

from apps.events.serializers import EventSerializer
from apps.moderation.models import FlagReport, ModerationLog


class FlagReportSerializer(serializers.ModelSerializer):
    reporter_email = serializers.ReadOnlyField(source="reporter.email")
    event_details = EventSerializer(source="event", read_only=True)

    class Meta:
        model = FlagReport
        fields = [
            "id",
            "event",
            "event_details",
            "reporter_email",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "created_at", "updated_at"]


class ModerationLogSerializer(serializers.ModelSerializer):
    moderator_email = serializers.ReadOnlyField(source="moderator.email")
    event_title = serializers.ReadOnlyField(source="event.title")

    class Meta:
        model = ModerationLog
        fields = [
            "id",
            "event",
            "event_title",
            "moderator_email",
            "action",
            "reason",
            "created_at",
        ]
