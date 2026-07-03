import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.notifications.models import NotificationPreference

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="notify@example.com",
        username="notifyuser",
        password="testpass123",  # pragma: allowlist secret
        first_name="Notify",
        last_name="User",
    )


@pytest.mark.django_db
class TestNotificationPreferenceView:
    def test_unauthenticated_returns_401(self, api_client):
        url = reverse("notification-preferences")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_creates_preferences_if_not_exists(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("notification-preferences")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["rsvp_confirmation"] is True
        assert response.data["event_reminder"] is True
        assert response.data["new_from_followed"] is True
        assert response.data["event_updates"] is True
        assert NotificationPreference.objects.filter(user=user).exists()

    def test_patch_updates_preferences(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("notification-preferences")
        response = api_client.patch(url, {"rsvp_confirmation": False}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["rsvp_confirmation"] is False
        pref = NotificationPreference.objects.get(user=user)
        assert pref.rsvp_confirmation is False

    def test_patch_multiple_fields(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("notification-preferences")
        payload = {
            "rsvp_confirmation": False,
            "event_reminder": False,
            "new_from_followed": False,
            "event_updates": False,
        }
        response = api_client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        pref = NotificationPreference.objects.get(user=user)
        assert pref.rsvp_confirmation is False
        assert pref.event_reminder is False
        assert pref.new_from_followed is False
        assert pref.event_updates is False

    def test_put_updates_all_preferences(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("notification-preferences")
        payload = {
            "rsvp_confirmation": True,
            "event_reminder": False,
            "new_from_followed": True,
            "event_updates": False,
        }
        response = api_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        pref = NotificationPreference.objects.get(user=user)
        assert pref.event_reminder is False
        assert pref.event_updates is False

    def test_second_get_does_not_create_duplicate(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("notification-preferences")
        api_client.get(url)
        api_client.get(url)
        assert NotificationPreference.objects.filter(user=user).count() == 1


@pytest.mark.django_db
class TestNotificationPreferenceModel:
    def test_str_representation(self, user):
        pref = NotificationPreference.objects.create(user=user)
        assert str(pref) == f"NotificationPreference({user.pk})"

    def test_default_all_true(self, user):
        pref = NotificationPreference.objects.create(user=user)
        assert pref.rsvp_confirmation is True
        assert pref.event_reminder is True
        assert pref.new_from_followed is True
        assert pref.event_updates is True
