# Substantive moderation tests live in test_moderation.py in this directory.
# This file contains model-level smoke tests to satisfy pytest collection.

import pytest
from django.contrib.auth import get_user_model

from apps.events.models import Event, EventStatus
from apps.moderation.models import FlagReport, FlagStatus, ModerationAction, ModerationLog
from apps.universities.models import University

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="mod_smoke@example.com",
        username="modsmokeuser",
        password="testpass123",  # pragma: allowlist secret
    )


@pytest.fixture
def event(db, user):
    univ = University.objects.create(name="Smoke University", domain="smoke.edu")
    evt = Event.objects.create(
        title="Smoke Test Event",
        organizer=user,
        status=EventStatus.APPROVED,
    )
    evt.universities.add(univ)
    return evt


@pytest.mark.django_db
class TestModerationModels:
    def test_flag_report_creation(self, user, event):
        report = FlagReport.objects.create(
            event=event, reporter=user, reason="Inappropriate content"
        )
        assert report.status == FlagStatus.PENDING
        assert str(report) == f"Flag on {event.title} by {user.email} (PENDING)"

    def test_moderation_log_creation(self, user, event):
        log = ModerationLog.objects.create(
            event=event,
            moderator=user,
            action=ModerationAction.APPROVED,
            reason="Meets guidelines",
        )
        assert log.action == ModerationAction.APPROVED
        assert str(log) == f"APPROVED on {event.title} by {user}"

    def test_flag_status_transitions(self, user, event):
        report = FlagReport.objects.create(event=event, reporter=user, reason="Spam")
        assert report.status == FlagStatus.PENDING
        report.status = FlagStatus.RESOLVED
        report.save()
        report.refresh_from_db()
        assert report.status == FlagStatus.RESOLVED
