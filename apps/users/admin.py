from django.contrib import admin

from apps.users.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ["pk", "email", "username", "display_users", "birthday"]
    list_filter = ["email", "username"]
    search_fields = ["email", "username"]

    def display_users(self, obj):
        return f"{obj.first_name} {obj.last_name} {obj.middle_name}"

    display_users.short_description = "ФИО"