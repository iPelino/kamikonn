from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class University(TimeStampedModel):
    name = models.CharField(_("name"), max_length=255, unique=True)
    short_name = models.CharField(_("short name"), max_length=50, unique=True)
    domain = models.CharField(
        _("domain"), max_length=255, unique=True, help_text=_("e.g. alu.edu.rw")
    )
    logo_url = models.URLField(_("logo URL"), blank=True)
    is_active = models.BooleanField(_("is active"), default=True)
    moderators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="moderated_universities",
        blank=True,
        verbose_name=_("moderators"),
    )

    class Meta:
        verbose_name_plural = "Universities"
        ordering = ["name"]

    def __str__(self):
        return self.name
