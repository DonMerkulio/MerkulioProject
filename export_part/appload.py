import requests
from django.http import HttpResponse


def photo_redactor(data):
    string = []


    for item in data:
        string.append(f'https://admin.avaxmotors.ru{item.get('url')}')
    if string == []:
        return ''
    else:
        string = ','.join(string)
        return string


def check_value(field):
    if field is None:
        return ''
    else:
        return field.get('value')


def check_display_value(field):
    if field is None:
        return ''
    else:
        return field.get('display_value')


def download_api() -> dict:
    url = 'https://admin.avaxmotors.ru/api/items.php?action=list&limit=100000&filters[stock_status]=0&with_photo=1'
    result = []
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        items = response['data'].get('items')
        # return(items)
        for item in items:
            res = {
                # 'Артикул': f'{check_display_value(item['fields'].get('shrot_id'))}{check_value(item['fields'].get('input_article'))}',
                'Артикул': item.get('article'),
                'VRN': check_value(item['fields'].get('vrn_number')),
                'Склад': check_display_value(item['fields'].get('stock_id')),
                'Запчасть': check_display_value(item['fields'].get('part_id')),
                'Марка': check_display_value(item['fields'].get('car_brand_id')),
                'Модель': check_display_value(item['fields'].get('car_model_id')),
                'Поколение': check_display_value(item['fields'].get('car_generation_id')),
                'Год': check_value(item['fields'].get('year')),
                'Маркировка двигателя': check_display_value(item['fields']),
                'Кузов': check_display_value(item['fields'].get('body_id')),
                'Объём': check_display_value(item['fields'].get('capacity_id')),
                'Особенность': check_display_value(item['fields'].get('peculiarities_id')),
                'Тип двигателя': check_display_value(item['fields'].get('type_id')),
                'КПП': check_display_value(item['fields'].get('kpp_id')),
                'Привод': check_display_value(item['fields'].get('drive_id')),
                'Примечание': check_value(item['fields'].get('description')),
                'OEM': check_value(item['fields'].get('oem_number')),
                'Цена': item['fields'].get('price_dollar'),
                'VIN': check_value(item['fields'].get('vin_number')),
                'Фото': photo_redactor(item['photos']),
            }
            result.append(res)
        return result
    else:
        return HttpResponse("Ошибка при получении данных с API", status=500)


download_api()
