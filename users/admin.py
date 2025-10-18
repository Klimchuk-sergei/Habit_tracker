from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "telegram_chat_id")
    list_filter = ("user",)
    search_fields = ("user__username", "telegram_chat_id")
