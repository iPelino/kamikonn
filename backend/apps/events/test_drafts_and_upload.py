import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.events.models import Event, EventStatus

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_create_event_draft_incomplete():
    client = APIClient()
    user = User.objects.create_user(
        username="test_draft",
        email="draft_user@test.com",
        password="pwd",  # pragma: allowlist secret
    )
    client.force_authenticate(user=user)

    url = reverse("event-list")
    data = {"title": "My Draft Event", "is_virtual": True}

    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == EventStatus.DRAFT
    assert response.data["start_time"] is None


def test_submit_draft_incomplete_fails():
    client = APIClient()
    user = User.objects.create_user(
        username="submit1",
        email="submit1@test.com",
        password="pwd",  # pragma: allowlist secret
    )
    client.force_authenticate(user=user)

    event = Event.objects.create(title="Incomplete Draft", organizer=user, status=EventStatus.DRAFT)

    url = reverse("event-submit", kwargs={"slug": event.slug})
    response = client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Missing required fields" in response.data["error"]


def test_submit_draft_complete_success():
    from datetime import timedelta

    from django.utils import timezone

    client = APIClient()
    user = User.objects.create_user(
        username="submit2",
        email="submit2@test.com",
        password="pwd",  # pragma: allowlist secret
    )
    client.force_authenticate(user=user)

    event = Event.objects.create(
        title="Complete Draft",
        organizer=user,
        status=EventStatus.DRAFT,
        start_time=timezone.now() + timedelta(days=1),
        end_time=timezone.now() + timedelta(days=1, hours=2),
        location="Kigali",
        description="A nice event",
    )

    url = reverse("event-submit", kwargs={"slug": event.slug})
    response = client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "submitted"

    event.refresh_from_db()
    assert event.status == EventStatus.PENDING


def test_banner_image_resizing():
    import io

    from PIL import Image

    img = Image.new("RGB", (2000, 1000), color="red")
    img_io = io.BytesIO()
    img.save(img_io, format="JPEG")
    img_io.seek(0)

    large_image = SimpleUploadedFile("large_banner.jpg", img_io.read(), content_type="image/jpeg")

    user = User.objects.create_user(
        username="img_user",
        email="img_user@test.com",
        password="pwd",  # pragma: allowlist secret
    )
    event = Event.objects.create(
        title="Image Resizing Test", organizer=user, banner_image=large_image
    )

    resized_img = Image.open(event.banner_image)
    assert resized_img.width <= 1200
    assert resized_img.height <= 630
