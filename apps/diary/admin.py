from django.contrib import admin

from apps.diary.models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ["pk","author", "title", "created_at", "updated_at"]
    list_filter = ["author", "title"]
    search_fields = ["author", "title"]
