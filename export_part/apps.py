from django.apps import AppConfig


class ExportPartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'export_part'

    def ready(self):
        pass
