from django.contrib import admin
from .models import AllRealTimeTicker


class AllRealTimeTickerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AllRealTimeTicker._meta.fields if field.name != 'id']
    list_filter = ['symbol_tree',
                   ]
    search_fields = ['symbol']
    date_hierarchy = 'updated_at'
    save_on_top = True


admin.site.register(AllRealTimeTicker, AllRealTimeTickerAdmin)