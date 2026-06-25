from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(_("name"), max_length=100, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)
    icon = models.CharField(
        _("icon name"), max_length=50, blank=True, help_text=_("Lucide icon name")
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class EventStatus(models.TextChoices):
    DRAFT = "DRAFT", _("Draft")
    PENDING = "PENDING", _("Pending Approval")
    APPROVED = "APPROVED", _("Approved")
    REJECTED = "REJECTED", _("Rejected")
    CANCELLED = "CANCELLED", _("Cancelled")


class Event(TimeStampedModel):
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, blank=True)
    description = models.TextField(_("description"), blank=True)

    start_time = models.DateTimeField(_("start time"), blank=True, null=True)
    end_time = models.DateTimeField(_("end time"), blank=True, null=True)

    location = models.CharField(_("location"), max_length=255, blank=True)
    is_virtual = models.BooleanField(_("is virtual"), default=False)
    virtual_link = models.URLField(_("virtual link"), blank=True)

    banner_image = models.ImageField(
        _("banner image"), upload_to="events/banners/", blank=True, null=True
    )

    status = models.CharField(
        _("status"), max_length=20, choices=EventStatus.choices, default=EventStatus.DRAFT
    )

    capacity = models.PositiveIntegerField(
        _("capacity"), default=0, help_text=_("0 means unlimited")
    )

    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, default=0.00)
    payment_link = models.URLField(_("payment link"), blank=True)

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
        verbose_name=_("organizer"),
    )

    category = models.ForeignKey(
        "events.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        verbose_name=_("category"),
    )
    universities = models.ManyToManyField(
        "universities.University", related_name="events", verbose_name=_("universities")
    )

    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        ordering = ["-start_time"]
        indexes = [
            GinIndex(fields=["search_vector"]),
            GinIndex(fields=["title"], opclasses=["gin_trgm_ops"], name="event_title_trgm_idx"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Resize banner image if provided
        if self.banner_image and not getattr(self, "_banner_resized", False):
            import os
            from io import BytesIO

            from django.core.files.base import ContentFile
            from PIL import Image

            try:
                img = Image.open(self.banner_image)
                max_size = (1200, 630)
                if img.height > max_size[1] or img.width > max_size[0]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    output = BytesIO()
                    img.save(output, format="JPEG", quality=85)
                    output.seek(0)
                    name = os.path.splitext(self.banner_image.name)[0] + ".jpg"
                    self.banner_image = ContentFile(output.read(), name=name)
                    self._banner_resized = True
            except Exception:
                pass

        super().save(*args, **kwargs)


class RSVPStatus(models.TextChoices):
    ATTENDING = "ATTENDING", _("Attending")
    WAITLISTED = "WAITLISTED", _("Waitlisted")
    CANCELLED = "CANCELLED", _("Cancelled")


class RSVP(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rsvps"
    )
    status = models.CharField(
        max_length=20, choices=RSVPStatus.choices, default=RSVPStatus.ATTENDING
    )

    class Meta:
        unique_together = [["event", "user"]]
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user} - {self.event} ({self.status})"


class SavedEvent(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="saves")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_events"
    )

    class Meta:
        unique_together = [["event", "user"]]
