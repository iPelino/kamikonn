from django.contrib import admin

from .models import OrganizerProfile


@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "trust_tier", "is_verified", "successful_events_count")
    list_filter = ("trust_tier", "is_verified")
    search_fields = ("user__email", "user__first_name", "user__last_name", "bio")
    readonly_fields = ("successful_events_count",)
