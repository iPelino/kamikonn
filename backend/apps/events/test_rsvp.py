"""
Tests for RSVP and SavedEvent functionality (Issue #26).
"""

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.events.models import RSVP, Event, EventStatus, RSVPStatus, SavedEvent

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="rsvp_user",
        email="rsvpuser@example.com",
        password="password123",  # pragma: allowlist secret
    )


@pytest.fixture
def other_user(django_user_model):
    return django_user_model.objects.create_user(
        username="other_user",
        email="other@example.com",
        password="password123",  # pragma: allowlist secret
    )


@pytest.fixture
def approved_event(user):
    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=2)
    return Event.objects.create(
        title="Approved Test Event",
        description="A great test event",
        start_time=start,
        end_time=end,
        location="Main Hall",
        organizer=user,
        status=EventStatus.APPROVED,
        capacity=0,  # unlimited by default
    )


@pytest.fixture
def capped_event(user):
    """An event with capacity of 2."""
    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=2)
    return Event.objects.create(
        title="Capped Event",
        description="Only 2 seats",
        start_time=start,
        end_time=end,
        location="Small Room",
        organizer=user,
        status=EventStatus.APPROVED,
        capacity=2,
    )


def _rsvp_url(event_slug: str) -> str:
    return reverse("event-rsvp-rsvp", kwargs={"event_slug": event_slug})


def _rsvp_cancel_url(event_slug: str) -> str:
    # POST and DELETE share the same URL path.
    return reverse("event-rsvp-rsvp", kwargs={"event_slug": event_slug})


def _calendar_url(event_slug: str) -> str:
    return reverse("event-rsvp-calendar", kwargs={"event_slug": event_slug})


def _save_url(event_slug: str) -> str:
    return reverse("event-save-save-event", kwargs={"event_slug": event_slug})


# ---------------------------------------------------------------------------
# RSVP tests
# ---------------------------------------------------------------------------


class TestRSVPUnlimitedCapacity:
    def test_rsvp_unlimited_event_gets_attending_status(self, api_client, user, approved_event):
        """RSVP to an unlimited event (capacity=0) assigns ATTENDING status."""
        api_client.force_authenticate(user=user)
        resp = api_client.post(_rsvp_url(approved_event.slug), format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.json()
        assert data["status"] == RSVPStatus.ATTENDING

    def test_rsvp_creates_db_record(self, api_client, user, approved_event):
        api_client.force_authenticate(user=user)
        api_client.post(_rsvp_url(approved_event.slug), format="json")
        assert RSVP.objects.filter(event=approved_event, user=user).exists()


class TestRSVPWithCapacity:
    def test_rsvp_within_capacity_gets_attending(self, api_client, user, capped_event):
        """First RSVP on a capped event gets ATTENDING."""
        api_client.force_authenticate(user=user)
        resp = api_client.post(_rsvp_url(capped_event.slug), format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()["status"] == RSVPStatus.ATTENDING

    def test_rsvp_over_capacity_gets_waitlisted(
        self, api_client, user, other_user, django_user_model, capped_event
    ):
        """Third RSVP on an event with capacity=2 is WAITLISTED."""
        # Fill capacity.
        third_user = django_user_model.objects.create_user(
            username="third_user",
            email="third@example.com",
            password="password123",  # pragma: allowlist secret
        )
        RSVP.objects.create(event=capped_event, user=user, status=RSVPStatus.ATTENDING)
        RSVP.objects.create(event=capped_event, user=other_user, status=RSVPStatus.ATTENDING)

        api_client.force_authenticate(user=third_user)
        resp = api_client.post(_rsvp_url(capped_event.slug), format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()["status"] == RSVPStatus.WAITLISTED

    def test_full_event_waitlists_new_rsvp(self, api_client, user, other_user, capped_event):
        """With capacity=2 and 2 ATTENDING, a new RSVP becomes WAITLISTED."""
        RSVP.objects.create(event=capped_event, user=user, status=RSVPStatus.ATTENDING)
        RSVP.objects.create(event=capped_event, user=other_user, status=RSVPStatus.ATTENDING)

        from django.contrib.auth import get_user_model

        User = get_user_model()
        extra_user = User.objects.create_user(
            username="extra_user",
            email="extra@example.com",
            password="password123",  # pragma: allowlist secret
        )
        api_client.force_authenticate(user=extra_user)
        resp = api_client.post(_rsvp_url(capped_event.slug), format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()["status"] == RSVPStatus.WAITLISTED


class TestRSVPCancellation:
    def test_cancel_rsvp_returns_204(self, api_client, user, approved_event):
        RSVP.objects.create(event=approved_event, user=user, status=RSVPStatus.ATTENDING)
        api_client.force_authenticate(user=user)
        resp = api_client.delete(_rsvp_cancel_url(approved_event.slug))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_cancel_promotes_first_waitlisted_user(
        self, api_client, user, other_user, capped_event
    ):
        """Cancelling an ATTENDING RSVP promotes the oldest WAITLISTED user."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        waitlisted_user = User.objects.create_user(
            username="waitlisted_user",
            email="waitlist@example.com",
            password="password123",  # pragma: allowlist secret
        )

        # Fill capacity.
        user_rsvp = RSVP.objects.create(event=capped_event, user=user, status=RSVPStatus.ATTENDING)
        RSVP.objects.create(event=capped_event, user=other_user, status=RSVPStatus.ATTENDING)
        # Waitlisted user.
        waitlisted_rsvp = RSVP.objects.create(
            event=capped_event, user=waitlisted_user, status=RSVPStatus.WAITLISTED
        )

        # Cancel user's RSVP, freeing a slot.
        api_client.force_authenticate(user=user)
        resp = api_client.delete(_rsvp_cancel_url(capped_event.slug))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        user_rsvp.refresh_from_db()
        assert user_rsvp.status == RSVPStatus.CANCELLED

        waitlisted_rsvp.refresh_from_db()
        assert waitlisted_rsvp.status == RSVPStatus.ATTENDING

    def test_cancel_unlimited_event_does_not_promote(
        self, api_client, user, other_user, approved_event
    ):
        """Cancelling on an unlimited event does not error and leaves waitlist unchanged."""
        RSVP.objects.create(event=approved_event, user=user, status=RSVPStatus.ATTENDING)
        api_client.force_authenticate(user=user)
        resp = api_client.delete(_rsvp_cancel_url(approved_event.slug))
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_cancel_nonexistent_rsvp_returns_404(self, api_client, user, approved_event):
        api_client.force_authenticate(user=user)
        resp = api_client.delete(_rsvp_cancel_url(approved_event.slug))
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDuplicateRSVP:
    def test_duplicate_rsvp_returns_400(self, api_client, user, approved_event):
        """A second RSVP from the same user to the same event returns 400."""
        RSVP.objects.create(event=approved_event, user=user, status=RSVPStatus.ATTENDING)
        api_client.force_authenticate(user=user)
        resp = api_client.post(_rsvp_url(approved_event.slug), format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "Already RSVPed" in resp.json()["detail"]

    def test_cancelled_then_new_rsvp_is_allowed(self, api_client, user, approved_event):
        """After cancelling, a user can RSVP again (updates the existing record)."""
        RSVP.objects.create(event=approved_event, user=user, status=RSVPStatus.CANCELLED)
        api_client.force_authenticate(user=user)
        resp = api_client.post(_rsvp_url(approved_event.slug), format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json()["status"] == RSVPStatus.ATTENDING
        # Should update the existing record, not create a new one.
        assert RSVP.objects.filter(event=approved_event, user=user).count() == 1


class TestCalendarDownload:
    def test_calendar_returns_ics(self, api_client, user, approved_event):
        api_client.force_authenticate(user=user)
        resp = api_client.get(_calendar_url(approved_event.slug))
        assert resp.status_code == status.HTTP_200_OK
        assert "text/calendar" in resp["Content-Type"]
        assert b"BEGIN:VCALENDAR" in resp.content
        assert b"BEGIN:VEVENT" in resp.content

    def test_calendar_contains_event_title(self, api_client, user, approved_event):
        api_client.force_authenticate(user=user)
        resp = api_client.get(_calendar_url(approved_event.slug))
        assert approved_event.title.encode() in resp.content


# ---------------------------------------------------------------------------
# SavedEvent tests
# ---------------------------------------------------------------------------


class TestSavedEvent:
    def test_save_event_creates_record(self, api_client, user, approved_event):
        api_client.force_authenticate(user=user)
        resp = api_client.post(_save_url(approved_event.slug), format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert SavedEvent.objects.filter(event=approved_event, user=user).exists()

    def test_save_event_duplicate_returns_400(self, api_client, user, approved_event):
        SavedEvent.objects.create(event=approved_event, user=user)
        api_client.force_authenticate(user=user)
        resp = api_client.post(_save_url(approved_event.slug), format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_unsave_event_removes_record(self, api_client, user, approved_event):
        SavedEvent.objects.create(event=approved_event, user=user)
        api_client.force_authenticate(user=user)
        resp = api_client.delete(_save_url(approved_event.slug))
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert not SavedEvent.objects.filter(event=approved_event, user=user).exists()

    def test_unsave_nonexistent_returns_404(self, api_client, user, approved_event):
        api_client.force_authenticate(user=user)
        resp = api_client.delete(_save_url(approved_event.slug))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_unauthenticated_save_returns_401(self, api_client, approved_event):
        resp = api_client.post(_save_url(approved_event.slug), format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
