import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from .models import OrganizerProfile, TrustTier

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="test_organizer@kamikonn.com",
        password="testpassword123",  # pragma: allowlist secret
        first_name="Test",
        last_name="Organizer",
    )


@pytest.mark.django_db
def test_become_organizer(client, user):
    client.force_login(user)

    url = reverse("organizers:become_organizer")
    data = {"bio": "I love organizing events.", "website": "https://example.com"}

    response = client.post(url, data, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED
    assert OrganizerProfile.objects.filter(user=user).exists()

    profile = OrganizerProfile.objects.get(user=user)
    assert profile.bio == "I love organizing events."
    assert profile.website == "https://example.com"
    assert profile.trust_tier == TrustTier.NEW


@pytest.mark.django_db
def test_become_organizer_already_exists(client, user):
    OrganizerProfile.objects.create(user=user, bio="Existing bio")
    client.force_login(user)

    url = reverse("organizers:become_organizer")
    data = {"bio": "New bio"}

    response = client.post(url, data, content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User is already an organizer."}


@pytest.mark.django_db
def test_get_current_organizer_profile(client, user):
    OrganizerProfile.objects.create(user=user, bio="Current user bio")
    client.force_login(user)

    url = reverse("organizers:current_organizer")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["bio"] == "Current user bio"
    assert response.json()["email"] == user.email


@pytest.mark.django_db
def test_get_organizer_detail(client, user):
    OrganizerProfile.objects.create(user=user, bio="Detail user bio")

    url = reverse("organizers:organizer_detail", kwargs={"user_id": user.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["bio"] == "Detail user bio"
    assert response.json()["email"] == user.email
