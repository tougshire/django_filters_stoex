from django.contrib import admin
from .models import FilterStore


class FilterStoreAdmin(admin.ModelAdmin):
    list_display = ["get_name", "user", "app_name", "model_name", "last_used"]


admin.site.register(FilterStore, FilterStoreAdmin)
