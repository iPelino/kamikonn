import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.events.models import Event, EventStatus
from apps.moderation.models import FlagReport, FlagStatus, ModerationAction, ModerationLog
from apps.universities.models import University

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password",  # pragma: allowlist secret
    )


@pytest.fixture
def moderator(django_user_model):
    return django_user_model.objects.create_user(
        username="moduser",
        email="mod@example.com",
        password="password",  # pragma: allowlist secret
    )


@pytest.fixture
def university(moderator):
    univ = University.objects.create(name="Test University", domain="example.edu")
    univ.moderators.add(moderator)
    return univ


@pytest.fixture
def event(user, university):
    evt = Event.objects.create(
        title="Test Event",
        description="A great event",
        organizer=user,
        status=EventStatus.APPROVED,
    )
    evt.universities.add(university)
    return evt


def test_user_can_flag_event(api_client, user, event):
    api_client.force_authenticate(user=user)
    url = reverse("moderation:flag-list")
    response = api_client.post(url, {"event": event.id, "reason": "Spam event"})

    assert response.status_code == status.HTTP_201_CREATED
    assert FlagReport.objects.count() == 1
    report = FlagReport.objects.first()
    assert report.reason == "Spam event"
    assert report.status == FlagStatus.PENDING

    assert ModerationLog.objects.count() == 1
    log = ModerationLog.objects.first()
    assert log.action == ModerationAction.FLAGGED
    assert log.reason == "Spam event"


def test_moderator_can_resolve_flag(api_client, moderator, event, user):
    report = FlagReport.objects.create(
        event=event, reporter=user, reason="Spam", status=FlagStatus.PENDING
    )

    api_client.force_authenticate(user=moderator)
    url = reverse("moderation:flag-resolve", kwargs={"pk": report.id})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    report.refresh_from_db()
    assert report.status == FlagStatus.RESOLVED

    log = ModerationLog.objects.filter(action=ModerationAction.FLAG_RESOLVED).first()
    assert log is not None
    assert log.moderator == moderator


def test_moderator_can_dismiss_flag(api_client, moderator, event, user):
    report = FlagReport.objects.create(
        event=event, reporter=user, reason="Spam", status=FlagStatus.PENDING
    )

    api_client.force_authenticate(user=moderator)
    url = reverse("moderation:flag-dismiss", kwargs={"pk": report.id})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    report.refresh_from_db()
    assert report.status == FlagStatus.DISMISSED

    log = ModerationLog.objects.filter(action=ModerationAction.FLAG_DISMISSED).first()
    assert log is not None
    assert log.moderator == moderator


def test_moderator_approve_event_logs_action(api_client, moderator, event):
    event.status = EventStatus.PENDING
    event.save()

    api_client.force_authenticate(user=moderator)
    url = reverse("moderation-event-approve", kwargs={"slug": event.slug})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    log = ModerationLog.objects.filter(action=ModerationAction.APPROVED).first()
    assert log is not None
    assert log.moderator == moderator
    assert log.event == event


def test_moderator_reject_event_logs_action(api_client, moderator, event):
    event.status = EventStatus.PENDING
    event.save()

    api_client.force_authenticate(user=moderator)
    url = reverse("moderation-event-reject", kwargs={"slug": event.slug})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    log = ModerationLog.objects.filter(action=ModerationAction.REJECTED).first()
    assert log is not None
    assert log.moderator == moderator
    assert log.event == event


def test_auto_trust_tier(api_client, user):
    # User has 3 clean events
    for i in range(3):
        Event.objects.create(
            title=f"Old Event {i}",
            description="A great event",
            organizer=user,
            status=EventStatus.APPROVED,
        )

    # Submit a new event
    new_event = Event.objects.create(
        title="New Event",
        description="A great new event",
        start_time="2026-12-01T10:00:00Z",
        end_time="2026-12-01T12:00:00Z",
        location="Campus",
        organizer=user,
        status=EventStatus.DRAFT,
    )

    api_client.force_authenticate(user=user)
    url = reverse("event-submit", kwargs={"slug": new_event.slug})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "approved_auto"

    new_event.refresh_from_db()
    assert new_event.status == EventStatus.APPROVED


def test_no_auto_trust_tier(api_client, user):
    # User has 2 clean events
    for i in range(2):
        Event.objects.create(
            title=f"Old Event {i}",
            description="A great event",
            organizer=user,
            status=EventStatus.APPROVED,
        )

    # Submit a new event
    new_event = Event.objects.create(
        title="New Event",
        description="A great new event",
        start_time="2026-12-01T10:00:00Z",
        end_time="2026-12-01T12:00:00Z",
        location="Campus",
        organizer=user,
        status=EventStatus.DRAFT,
    )

    api_client.force_authenticate(user=user)
    url = reverse("event-submit", kwargs={"slug": new_event.slug})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "submitted"

    new_event.refresh_from_db()
    assert new_event.status == EventStatus.PENDING
