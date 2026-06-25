from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class TrustTier(models.IntegerChoices):
    NEW = 1, _("New Organizer")
    TRUSTED = 2, _("Trusted Organizer")
    VERIFIED = 3, _("Verified Partner")


class OrganizerProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organizer_profile",
        verbose_name=_("user"),
    )
    bio = models.TextField(_("bio"), blank=True)
    website = models.URLField(_("website"), blank=True)
    social_links = models.JSONField(_("social links"), default=dict, blank=True)

    trust_tier = models.IntegerField(
        _("trust tier"), choices=TrustTier.choices, default=TrustTier.NEW
    )
    is_verified = models.BooleanField(_("is verified"), default=False)

    # Track clean events for auto-trust progression
    successful_events_count = models.PositiveIntegerField(
        _("successful events count"),
        default=0,
        help_text=_("Number of approved events without flags. Reaching 3 unlocks TRUSTED tier."),
    )

    class Meta:
        verbose_name = _("Organizer Profile")
        verbose_name_plural = _("Organizer Profiles")

    def __str__(self):
        return f"Organizer Profile for {self.user.email}"
