from django.core.management.base import BaseCommand
from export_part.models import ExportField


class Command(BaseCommand):
    help = "Инициализация данных для ExportField"

    def handle(self, *args, **kwargs):
        fields = [
            'id', 'ID_EXT', 'МАРКА', 'МОДЕЛЬ', 'ШРОТ', 'ГОД', 'ЗАПЧАСТЬ', 'ТОПЛИВО', 'ОБЪЕМ', 'ТИП ДВИГАТЕЛЯ',
            'КОРОБКА', 'ТИП КУЗОВА', 'ОРИГИНАЛЬНЫЙ НОМЕР', 'ОПИСАНИЕ', 'ЦЕНА', 'ВАЛЮТА', 'ФОТО', 'КАТЕГОРИЯ',
            'ПРИВОД', 'МАРКИРОВКА ДВИГАТЕЛЯ', 'ВХОДНОЙ АРТИКУЛ', 'VIN', 'Склад', 'ВИДЕО', 'ZAP_VIDEO', 'CAR_VIDEO',
        ]
        for field_name in fields:
            ExportField.objects.get_or_create(name=field_name)
        self.stdout.write(self.style.SUCCESS("ExportField инициализированы"))
