from django.contrib import admin
from checkins.models import MoodEntry

# admin.site.register(MoodEntry)

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ("score", "tag", "created_at")
    search_fields = ("reason",)
    list_filter = ("score",)
