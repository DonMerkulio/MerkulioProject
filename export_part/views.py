from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
import requests
import openpyxl
from openpyxl.styles import Font
import csv

from clients.models import Clients
from export_part.appload import download_api
from export_part.models import ExportField


# drom_fields = [
#     'Артикул', 'Наименование товара', 'Новый/б.у.', 'Марка', 'Модель', 'Кузов', 'Номер', 'Двигатель',
#     'Год', 'Цвет', 'Примечание', 'Количество', 'Цена', 'Наличие', 'Сроки доставки', 'Фотография'
# ]


class DownloadFileView(View):
    def get(self, request, key, file_type):
        # Проверяем, существует ли client с данным ключом
        client = get_object_or_404(Clients, key=key)

        # Получаем данные с API

        cars_data = download_api()


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



# class DownloadFileDromView(View):
#     """
#     GET /drom/csv/?api_url=https://example.com/api
#     Разделитель ';', BOM для Excel, переносы строк в "Примечание".
#     """
#     CSV_HEADERS = [
#         "Артикул",
#         "Наименование товара",
#         "Новый/б.у.",
#         "Марка",
#         "Модель",
#         "Кузов",
#         "Номер",
#         "Двигатель",
#         "Год",
#         "Цвет",
#         "Примечание",
#         "Количество",
#         "Цена",
#         "Наличие",
#         "Фотография",
#     ]
#
#     def get(self, request, key, file_type):
#         # Проверяем, существует ли client с данным ключом
#         client = get_object_or_404(Clients, key=key)
#         print(key, file_type)
#         # Получаем данные с API
#
#         response = requests.get(api_url)
#         print(request)
#         if response.status_code == 200:
#             cars_data = response.json()
#         else:
#             return HttpResponse("Ошибка при получении данных с API", status=500)
#
#         # В зависимости от типа файла, генерируем CSV или Excel
#         if file_type == 'csv':
#             return self.create_csv(request, cars_data)
#         else:
#             raise Http404("Файл не найден")
#
#     def create_csv(self, request, cars_data):
#         filename = f'drom_export.csv'
#         response = HttpResponse(content_type="text/csv; charset=utf-8")
#         response['Content-Disposition'] = 'attachment; filename=drom_data.csv'
#         response.write("\ufeff")  # BOM для Excel
#
#         writer = csv.writer(
#             response,
#             delimiter=";",
#             lineterminator="\r\n",
#             quoting=csv.QUOTE_MINIMAL,
#         )
#         writer.writerow(self.CSV_HEADERS)
#
#         for obj in cars_data:
#             val = self._val_from(obj)
#
#             artikel = val("ID_EXT")
#             name = val("ЗАПЧАСТЬ")
#             new_used = "б.у."
#             marka = val("МАРКА")
#             model = val("МОДЕЛЬ")
#             kuzov = val("ТИП КУЗОВА")
#
#             number = self._number_field(obj.get("ОРИГИНАЛЬНЫЙ НОМЕР"))
#             engine = val("МАРКИРОВКА ДВИГАТЕЛЯ")
#             year = val("ГОД")
#             color = ""
#             price = int(val("ЦЕНА")) * 85
#             stock = "В наличии"
#             photo = self._string_or_join(obj.get("ФОТО"))
#             opisanie = val("ОПИСАНИЕ")
#
#             # Примечание по шаблону
#             line1 = self._join_tokens(name, marka, model, year, engine)
#             lines = [
#                 line1,
#                 "Цена указана за запчасть в сборе!",
#                 opisanie,
#                 number,
#                 "Полный пакет документов для оформления в ГАИ",
#                 "Запчасть контрактная, cняты с аукционных автомобилей с минимальными пробегами.",
#                 "",  # пустая строка перед последней
#                 "Все контрактные автозапчасти в наличии!",
#             ]
#             note = "\n".join(x for x in lines if x is not None)
#
#             row = [
#                 artikel,
#                 name,
#                 new_used,
#                 marka,
#                 model,
#                 kuzov,
#                 number,
#                 engine,
#                 year,
#                 color,
#                 note,
#                 1,
#                 price,
#                 stock,
#                 photo,
#             ]
#             writer.writerow(row)
#
#         return response
#
#     @staticmethod
#     def _extract_items(payload):
#         if isinstance(payload, list):
#             return payload
#         if isinstance(payload, dict):
#             for k in ("data", "items", "results", "records"):
#                 v = payload.get(k)
#                 if isinstance(v, list):
#                     return v
#         return None
#
#     @staticmethod
#     def _val_from(obj):
#         def _val(key: str) -> str:
#             v = obj.get(key)
#             if v is None:
#                 return ""
#             if isinstance(v, (list, tuple)):
#                 return " ".join(str(x).strip() for x in v if x is not None).strip()
#             return str(v).strip()
#
#         return _val
#
#     @staticmethod
#     def _join_tokens(*tokens) -> str:
#         parts = [str(t).strip() for t in tokens if t is not None and str(t).strip()]
#         return " ".join(parts)
#
#     @staticmethod
#     def _string_or_join(value) -> str:
#         if value in (None, ""):
#             return ""
#         if isinstance(value, (list, tuple)):
#             return " ".join(str(x).strip() for x in value if x is not None).strip()
#         return str(value).strip()
#
#     @staticmethod
#     def _number_field(value) -> str:
#         """Заменяет ';' на пробел. Поддержка списка/кортежа/строки. Пусто если нет."""
#         if value in (None, ""):
#             return ""
#         if isinstance(value, (list, tuple)):
#             s = " ".join(str(x) for x in value if x is not None)
#         else:
#             s = str(value)
#         return s.replace(";", " ").strip()
