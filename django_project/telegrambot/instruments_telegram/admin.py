from django.contrib import admin
from .models import AboutUs, WelcomeMessage

# Register your models here.


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "language", "image_url_file_id", "video_url_file_id", "created_at", "updated_at")


@admin.register(WelcomeMessage)
class WelcomeMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "language", "image_url_file_id", "video_url_file_id", "created_at", "updated_at")


