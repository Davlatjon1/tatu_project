from django.contrib import admin

# Register your models here.
from django_project.telegrambot.contractors.models import Branch, Client
from django_project.telegrambot.usersmanage.models import Review


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid_1c', 'name', 'deletion_mark', 'branch', 'days_of_the_week', 'phone', 'address')
    list_display_links = ('id', 'name', 'branch')
    search_fields = ('id', 'name')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user__name', 'comment')


admin.site.register(Client, ClientAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Review, ReviewAdmin)
