from django.contrib import admin
from .models import University

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'domain', 'is_active', 'created_at')
    search_fields = ('name', 'short_name', 'domain')
    list_filter = ('is_active',)
