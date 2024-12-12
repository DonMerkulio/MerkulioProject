import random
import string

from django.contrib import admin

from clients.models import Clients


def generate_key():
    """Генерация случайного ключа длиной 8 символов"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


@admin.register(Clients)
class AdminClients(admin.ModelAdmin):
    list_display = ('name', 'url', 'export_url')

    def save_model(self, request, obj, form, change):
        if not obj.key:  # Генерировать ключ только если его нет
            obj.key = generate_key()
        super().save_model(request, obj, form, change)
