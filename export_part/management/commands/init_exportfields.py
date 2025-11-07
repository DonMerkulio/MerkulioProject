from django.core.management.base import BaseCommand
from export_part.models import ExportField


class Command(BaseCommand):
    help = "Инициализация данных для ExportField"

    def handle(self, *args, **kwargs):
        fields = [
            'Артикул', 'VRN', 'Склад', 'Запчасть', 'Марка', 'Модель', 'Поколение', 'Год',
            'Маркировка двигателя', 'Кузов', 'Объём', 'Особенность', 'Тип двигателя',
            'КПП', 'Привод', 'Примечание', 'OEM', 'Цена', 'VIN', 'Фото'
        ]
        for field_name in fields:
            ExportField.objects.get_or_create(name=field_name)
        self.stdout.write(self.style.SUCCESS("ExportField инициализированы"))
