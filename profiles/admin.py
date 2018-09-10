from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Profile, BinanceKey, TelegramBotSettings, TelegramChatIds


class ProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Profile


class ProfileAdmin(UserAdmin):
    form = ProfileChangeForm


class BinanceKeyAdmin(admin.ModelAdmin):
    # Include all fields except id and created_at
    list_display = [field.name for field in BinanceKey._meta.fields if field.name != 'id']


class TelegramBotSettingsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TelegramBotSettings._meta.fields if field.name != 'id']
    filter_horizontal = ['chat']

class TelegramChatIdsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TelegramChatIds._meta.fields if field.name != 'id']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(BinanceKey, BinanceKeyAdmin)
admin.site.register(TelegramBotSettings, TelegramBotSettingsAdmin)
admin.site.register(TelegramChatIds, TelegramChatIdsAdmin)