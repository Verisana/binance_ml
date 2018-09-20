from django.contrib import admin
from .models import BotSettings, OpenedDeals, ClosedDeals


class BotSettingsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BotSettings._meta.fields if field.name != 'id']


class OpenedDealsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OpenedDeals._meta.fields if field.name != 'id']


class ClosedDealsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClosedDeals._meta.fields if field.name != 'id']


admin.site.register(BotSettings, BotSettingsAdmin)
admin.site.register(OpenedDeals, OpenedDealsAdmin)
admin.site.register(ClosedDeals, ClosedDealsAdmin)