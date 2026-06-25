import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import OrganizerProfile, TrustTier

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testorg",
        email="test_organizer@kamikonn.com",
        password="testpassword123",  # pragma: allowlist secret
        first_name="Test",
        last_name="Organizer",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_become_organizer(api_client, user):
    api_client.force_authenticate(user=user)

    url = reverse("organizers:become_organizer")
    data = {"bio": "I love organizing events.", "website": "https://example.com"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert OrganizerProfile.objects.filter(user=user).exists()

    profile = OrganizerProfile.objects.get(user=user)
    assert profile.bio == "I love organizing events."
    assert profile.website == "https://example.com"
    assert profile.trust_tier == TrustTier.NEW


@pytest.mark.django_db
def test_become_organizer_already_exists(api_client, user):
    OrganizerProfile.objects.create(user=user, bio="Existing bio")
    api_client.force_authenticate(user=user)

    url = reverse("organizers:become_organizer")
    data = {"bio": "New bio"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User is already an organizer."}


@pytest.mark.django_db
def test_get_current_organizer_profile(api_client, user):
    OrganizerProfile.objects.create(user=user, bio="Current user bio")
    api_client.force_authenticate(user=user)

    url = reverse("organizers:current_organizer")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["bio"] == "Current user bio"
    assert response.json()["email"] == user.email


@pytest.mark.django_db
def test_get_organizer_detail(api_client, user):
    OrganizerProfile.objects.create(user=user, bio="Detail user bio")

    url = reverse("organizers:organizer_detail", kwargs={"user_id": user.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["bio"] == "Detail user bio"
    assert response.json()["email"] == user.email
