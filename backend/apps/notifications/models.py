from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class NotificationPreference(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
        verbose_name=_("user"),
    )
    rsvp_confirmation = models.BooleanField(_("RSVP confirmation emails"), default=True)
    event_reminder = models.BooleanField(_("24h event reminder emails"), default=True)
    new_from_followed = models.BooleanField(_("new events from followed organizers"), default=True)
    event_updates = models.BooleanField(_("event update notifications"), default=True)

    class Meta:
        verbose_name = _("Notification Preference")
        verbose_name_plural = _("Notification Preferences")

    def __str__(self) -> str:
        return f"NotificationPreference({self.user_id})"
