from django.contrib import admin
from .models import Link


def make_active(self, request, queryset):
    queryset.update(is_active=True)
make_active.short_description = "Активировать выбранные ссылки"

def make_inactive(self, request, queryset):
    queryset.update(is_active=False)
make_inactive.short_description = "Деактивировать выбранные ссылки"

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'short_url', 'clicks', 'created_at', 'is_active', 'user')
    search_fields = ('url', 'short_url')
    list_filter = ('is_active', 'user')
    readonly_fields = ('clicks', 'created_at')
    ordering = ('created_at',)
    actions = [make_active, make_inactive]
