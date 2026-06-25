from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import OrganizerProfile

User = get_user_model()


class OrganizerProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = OrganizerProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "bio",
            "website",
            "social_links",
            "trust_tier",
            "is_verified",
            "successful_events_count",
        ]
        read_only_fields = ["trust_tier", "is_verified", "successful_events_count"]


class BecomeOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerProfile
        fields = ["bio", "website", "social_links"]
