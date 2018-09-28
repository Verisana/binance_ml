from django.contrib import admin
from .models import BotSettings, Deals


class BotSettingsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BotSettings._meta.fields if field.name != 'id']


class DealsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Deals._meta.fields if field.name != 'id']



admin.site.register(BotSettings, BotSettingsAdmin)
admin.site.register(Deals, DealsAdmin)