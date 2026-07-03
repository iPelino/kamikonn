import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.events.models import RSVP, Event, EventStatus, RSVPStatus
from apps.universities.models import University

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="rsvpuser@example.com",
        username="rsvpuser",
        password="testpass123",  # pragma: allowlist secret
        first_name="RSVP",
        last_name="User",
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        email="other@example.com",
        username="otheruser",
        password="testpass123",  # pragma: allowlist secret
        first_name="Other",
        last_name="User",
    )


@pytest.fixture
def university(db):
    return University.objects.create(name="Test University", domain="test.edu")


@pytest.fixture
def event(db, user, university):
    evt = Event.objects.create(
        title="Campus Hackathon",
        description="A 24h coding competition",
        organizer=user,
        status=EventStatus.APPROVED,
        capacity=2,
        start_time="2026-12-01T09:00:00Z",
        end_time="2026-12-02T09:00:00Z",
    )
    evt.universities.add(university)
    return evt


@pytest.fixture
def unlimited_event(db, user, university):
    evt = Event.objects.create(
        title="Open Lecture",
        description="Open to everyone",
        organizer=user,
        status=EventStatus.APPROVED,
        capacity=0,
        start_time="2026-12-05T10:00:00Z",
    )
    evt.universities.add(university)
    return evt


@pytest.mark.django_db
class TestRSVPCreation:
    def test_rsvp_attending_below_capacity(self, api_client, user, event):
        api_client.force_authenticate(user=user)
        url = reverse("event-rsvp-rsvp", kwargs={"event_slug": event.slug})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        rsvp = RSVP.objects.get(event=event, user=user)
        assert rsvp.status == RSVPStatus.ATTENDING

    def test_rsvp_waitlisted_at_capacity(self, api_client, user, other_user, event):
        # Fill the 2-seat capacity with the organizer and one more user
        third_user = User.objects.create_user(
            email="third@example.com",
            username="thirduser",
            password="testpass123",  # pragma: allowlist secret
        )
        RSVP.objects.create(event=event, user=user, status=RSVPStatus.ATTENDING)
        RSVP.objects.create(event=event, user=other_user, status=RSVPStatus.ATTENDING)

        api_client.force_authenticate(user=third_user)
        url = reverse("event-rsvp-rsvp", kwargs={"event_slug": event.slug})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        rsvp = RSVP.objects.get(event=event, user=third_user)
        assert rsvp.status == RSVPStatus.WAITLISTED

    def test_rsvp_unlimited_event(self, api_client, user, unlimited_event):
        api_client.force_authenticate(user=user)
        url = reverse("event-rsvp-rsvp", kwargs={"event_slug": unlimited_event.slug})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        rsvp = RSVP.objects.get(event=unlimited_event, user=user)
        assert rsvp.status == RSVPStatus.ATTENDING

    def test_duplicate_rsvp_returns_400(self, api_client, user, event):
        RSVP.objects.create(event=event, user=user, status=RSVPStatus.ATTENDING)
        api_client.force_authenticate(user=user)
        url = reverse("event-rsvp-rsvp", kwargs={"event_slug": event.slug})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Already RSVPed" in response.data.get("detail", "")

    def test_unauthenticated_rsvp_returns_401(self, api_client, event):
        url = reverse("event-rsvp-rsvp", kwargs={"event_slug": event.slug})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRSVPCancellation:
    def test_cancel_rsvp(self, api_client, user, event):
        RSVP.objects.create(event=event, user=user, status=RSVPStatus.ATTENDING)
        api_client.force_authenticate(user=user)
        url = reverse("event-rsvp-rsvp", kwargs={"event_slug": event.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        rsvp = RSVP.objects.get(event=event, user=user)
        assert rsvp.status == RSVPStatus.CANCELLED

    def test_cancel_promotes_waitlisted_user(self, api_client, user, other_user, event):
        third_user = User.objects.create_user(
            email="waitlisted@example.com",
            username="waitlistuser",
            password="testpass123",  # pragma: allowlist secret
        )
        RSVP.objects.create(event=event, user=user, status=RSVPStatus.ATTENDING)
        RSVP.objects.create(event=event, user=other_user, status=RSVPStatus.ATTENDING)
        RSVP.objects.create(event=event, user=third_user, status=RSVPStatus.WAITLISTED)

        api_client.force_authenticate(user=user)
        url = reverse("event-rsvp-rsvp", kwargs={"event_slug": event.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        third_rsvp = RSVP.objects.get(event=event, user=third_user)
        assert third_rsvp.status == RSVPStatus.ATTENDING

    def test_cancel_nonexistent_rsvp_returns_404(self, api_client, user, event):
        api_client.force_authenticate(user=user)
        url = reverse("event-rsvp-rsvp", kwargs={"event_slug": event.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRSVPModel:
    def test_rsvp_str(self, user, event):
        rsvp = RSVP.objects.create(event=event, user=user, status=RSVPStatus.ATTENDING)
        assert str(rsvp) == f"{user} - {event} ({RSVPStatus.ATTENDING})"

    def test_rsvp_unique_constraint(self, user, event):
        from django.db import IntegrityError

        RSVP.objects.create(event=event, user=user, status=RSVPStatus.ATTENDING)
        with pytest.raises(IntegrityError):
            RSVP.objects.create(event=event, user=user, status=RSVPStatus.WAITLISTED)
