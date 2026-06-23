from django.db import models
from apps.core.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

class University(TimeStampedModel):
    name = models.CharField(_('name'), max_length=255, unique=True)
    short_name = models.CharField(_('short name'), max_length=50, unique=True)
    domain = models.CharField(_('domain'), max_length=255, unique=True, help_text=_("e.g. alu.edu.rw"))
    logo_url = models.URLField(_('logo URL'), blank=True)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name_plural = 'Universities'
        ordering = ['name']

    def __str__(self):
        return self.name
