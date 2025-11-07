from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
import requests
import openpyxl
from openpyxl.styles import Font
import csv

from clients.models import Clients
from export_part.models import ExportField


class DownloadFileView(View):
    def get(self, request, key, file_type):
        # Проверяем, существует ли client с данным ключом
        client = get_object_or_404(Clients, key=key)

        # Получаем данные с API
        api_url = "https://avax.by/api/all_zap/DueMQ88!Sm43"
        response = requests.get(api_url)

        if response.status_code == 200:
            cars_data = response.json()
        else:
            return HttpResponse("Ошибка при получении данных с API", status=500)

        # В зависимости от типа файла, генерируем CSV или Excel
        if file_type == 'csv':
            return self.generate_car_csv(request, cars_data)
        elif file_type == 'xlsx':
            return self.generate_car_xlsx(request, cars_data)
        else:
            raise Http404("Файл не найден")

    def get_included_fields(self):
        """Получить список включённых полей из модели ExportField."""
        return list(ExportField.objects.filter(is_included=True).values_list('name', flat=True))

    def generate_car_xlsx(self, request, cars_data):
        # Получаем список включённых полей
        included_fields = self.get_included_fields()

        # Создаём Excel-файл
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Part Data'
        ws.append(included_fields)

        # Добавляем данные в Excel
        for car in cars_data:
            row = [car.get(field, '') for field in included_fields]
            ws.append(row)

        # Форматируем заголовки
        for cell in ws[1]:
            cell.font = Font(bold=True)

        # Возвращаем файл в ответе
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=part_data.xlsx'
        wb.save(response)
        return response

    def generate_car_csv(self, request, cars_data):
        # Получаем список включённых полей
        included_fields = self.get_included_fields()

        # Создаём CSV-файл
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=part_data.csv'
        writer = csv.writer(response)
        writer.writerow(included_fields)

        # Добавляем данные в CSV
        for car in cars_data:
            row = [car.get(field, '') for field in included_fields]
            writer.writerow(row)

        return response
