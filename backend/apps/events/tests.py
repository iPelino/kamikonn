from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.events.models import Category, Event, EventStatus

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def category():
    return Category.objects.create(name="Technology", slug="technology", description="Tech events")


@pytest.fixture
def university():
    from apps.universities.models import University

    return University.objects.create(name="Test University", short_name="TU", domain="tu.edu.rw")


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123",  # pragma: allowlist secret
    )


@pytest.fixture
def event(user, category):
    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=2)
    return Event.objects.create(
        title="Sample Event",
        description="A great sample event",
        start_time=start,
        end_time=end,
        location="Main Hall",
        organizer=user,
        category=category,
        status=EventStatus.APPROVED,
    )


def test_event_slug_generation(user):
    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=2)
    e1 = Event.objects.create(
        title="Test Event Title",
        description="Desc",
        start_time=start,
        end_time=end,
        location="Loc",
        organizer=user,
    )
    assert e1.slug == "test-event-title"

    e2 = Event.objects.create(
        title="Test Event Title",
        description="Desc",
        start_time=start,
        end_time=end,
        location="Loc",
        organizer=user,
    )
    assert e2.slug == "test-event-title-1"


def test_event_list_unauthenticated(api_client, event):
    url = reverse("event-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # It should return APPROVED events
    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == event.title


def test_event_create_authenticated(api_client, user, category, university):
    api_client.force_authenticate(user=user)
    url = reverse("event-list")

    start = timezone.now() + timedelta(days=2)
    end = start + timedelta(hours=3)

    data = {
        "title": "New Event from API",
        "description": "Awesome API event",
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "location": "Virtual",
        "is_virtual": True,
        "category": category.id,
        "universities": [university.id],
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Event.objects.count() == 1

    new_event = Event.objects.get(title="New Event from API")
    assert new_event.organizer == user
    assert new_event.status == EventStatus.DRAFT
    assert new_event.universities.count() == 1
    assert new_event.category == category


def test_moderation_queue_access(api_client, user, university):
    # A regular user without moderation rights should not access the queue
    api_client.force_authenticate(user=user)
    url = reverse("moderation-event-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Assign user to be a moderator for the university
    university.moderators.add(user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_moderation_queue_lists_pending_events(api_client, user, category, university):
    university.moderators.add(user)
    api_client.force_authenticate(user=user)

    # Create one pending, one approved, one from another university
    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=2)

    pending_event = Event.objects.create(
        title="Pending Event",
        start_time=start,
        end_time=end,
        location="Loc",
        organizer=user,
        status=EventStatus.PENDING,
    )
    pending_event.universities.add(university)

    approved_event = Event.objects.create(
        title="Approved Event",
        start_time=start,
        end_time=end,
        location="Loc",
        organizer=user,
        status=EventStatus.APPROVED,
    )
    approved_event.universities.add(university)

    url = reverse("moderation-event-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == "Pending Event"


def test_moderation_approve_reject(api_client, user, university):
    university.moderators.add(user)
    api_client.force_authenticate(user=user)

    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=2)

    event1 = Event.objects.create(
        title="To Approve",
        start_time=start,
        end_time=end,
        location="Loc",
        organizer=user,
        status=EventStatus.PENDING,
    )
    event1.universities.add(university)

    event2 = Event.objects.create(
        title="To Reject",
        start_time=start,
        end_time=end,
        location="Loc",
        organizer=user,
        status=EventStatus.PENDING,
    )
    event2.universities.add(university)

    # Approve event1
    url_approve = reverse("moderation-event-approve", args=[event1.slug])
    resp1 = api_client.post(url_approve)
    assert resp1.status_code == status.HTTP_200_OK
    event1.refresh_from_db()
    assert event1.status == EventStatus.APPROVED

    # Reject event2
    url_reject = reverse("moderation-event-reject", args=[event2.slug])
    resp2 = api_client.post(url_reject)
    assert resp2.status_code == status.HTTP_200_OK
    event2.refresh_from_db()
    assert event2.status == EventStatus.REJECTED
