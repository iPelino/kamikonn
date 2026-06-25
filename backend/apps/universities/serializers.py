from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import University

User = get_user_model()


class UniversityModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]
        read_only_fields = fields


class UniversitySerializer(serializers.ModelSerializer):
    moderators = UniversityModeratorSerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = [
            "id",
            "name",
            "short_name",
            "domain",
            "logo_url",
            "is_active",
            "moderators",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "moderators"]
