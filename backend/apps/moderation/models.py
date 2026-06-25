from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.events.models import Event


class FlagStatus(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    RESOLVED = "RESOLVED", _("Resolved")
    DISMISSED = "DISMISSED", _("Dismissed")


class FlagReport(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="flag_reports")
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="flag_reports"
    )
    reason = models.TextField(_("reason"))
    status = models.CharField(
        _("status"), max_length=20, choices=FlagStatus.choices, default=FlagStatus.PENDING
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Flag on {self.event.title} by {self.reporter.email} ({self.status})"


class ModerationAction(models.TextChoices):
    APPROVED = "APPROVED", _("Approved Event")
    REJECTED = "REJECTED", _("Rejected Event")
    FLAGGED = "FLAGGED", _("Flagged Event")
    FLAG_RESOLVED = "FLAG_RESOLVED", _("Resolved Flag")
    FLAG_DISMISSED = "FLAG_DISMISSED", _("Dismissed Flag")


class ModerationLog(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="moderation_logs")
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="moderation_actions",
    )
    action = models.CharField(_("action"), max_length=20, choices=ModerationAction.choices)
    reason = models.TextField(_("reason"), blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} on {self.event.title} by {self.moderator}"
