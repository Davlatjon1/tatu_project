from django.contrib import admin
from django_project.telegrambot.constants.models import Restrict_Users_users, Restrict_Users_TGBOT, Constants, \
    SettingsAPI, Channel, Currency


class RestrictUsersUserInline(admin.TabularInline):
    model = Restrict_Users_users
    extra = 0
    autocomplete_fields = ['user']


class ChannelInline(admin.TabularInline):
    model = Channel
    extra = 0


class RestrictUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'days', 'all_users')
    list_filter = ['created_at']
    list_display_links = ('id', 'days')
    search_fields = ('id', 'name')
    inlines = [RestrictUsersUserInline]
    list_editable = ('enabled',)

    def all_users(self, _object: Constants, **kwargs):
        users_object = _object.disabled_users.values('user__name').all()[:3]
        users = [user['user__name'] for index, user in enumerate(users_object) if index < 2]
        return f"{', '.join(users)}{'...' if len(users) < len(users_object) else ''}"


@admin.register(SettingsAPI)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'login_1c')
    list_display_links = list_display


@admin.register(Constants)
class ConstantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'restrict_users', 'setting_api')
    list_filter = ['created_at']
    list_display_links = ('id', 'name', 'restrict_users', 'setting_api')
    search_fields = ('id',)
    autocomplete_fields = ['restrict_users']
    inlines = [ChannelInline]

    def has_add_permission(self, request):
        count = Constants.objects.count()
        if count == 0:
            return True
        return False


admin.site.register([Currency])
admin.site.register(Restrict_Users_TGBOT, RestrictUsersAdmin)
