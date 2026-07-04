from django.contrib import admin

from .models import Availability, Mentor


class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'subjects', 'field_of_study', 'mentoring_format')
    search_fields = ('name', 'subjects', 'field_of_study')
    list_filter = ('mentoring_format', 'field_of_study')
    inlines = [AvailabilityInline]
