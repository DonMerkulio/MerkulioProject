from django.contrib import admin
from export_part.models import ExportField


@admin.register(ExportField)
class ExportFieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_included']
    list_editable = ['is_included']
    ordering = ['name']
    search_fields = ['name']
