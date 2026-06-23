from rest_framework import serializers

from apps.events.models import Category, Event
from apps.universities.models import University


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "icon"]


class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.ReadOnlyField(source="organizer.get_full_name")
    category_name = serializers.ReadOnlyField(source="category.name")
    universities = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(), many=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "start_time",
            "end_time",
            "location",
            "is_virtual",
            "virtual_link",
            "banner_image",
            "status",
            "capacity",
            "price",
            "payment_link",
            "organizer",
            "organizer_name",
            "category",
            "category_name",
            "universities",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "status", "organizer"]

    def create(self, validated_data):
        universities = validated_data.pop("universities", [])
        event = Event.objects.create(**validated_data)
        event.universities.set(universities)
        return event

    def update(self, instance, validated_data):
        universities = validated_data.pop("universities", None)
        event = super().update(instance, validated_data)
        if universities is not None:
            event.universities.set(universities)
        return event
