from django.db import models


class Clients(models.Model):
    class Meta:
        verbose_name = 'Клиента'
        verbose_name_plural = 'Клиенты'

    name = models.CharField(verbose_name='Имя', max_length=255)
    url = models.CharField(verbose_name='Ссылка на магазин', max_length=255)
    key = models.CharField(verbose_name='Ключ', max_length=10, unique=True, blank=True)
    export_url_xlsx = models.CharField(verbose_name='Ссылка для клиента xlsx', max_length=255, blank=True)
    export_url_csv = models.CharField(verbose_name='Ссылка для клиента csv', max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.export_url:  # Генерировать ключ только если его нет
            self.export_url_xlsx = f'www.merkulio.site/export/{self.key}/xlsx'
            self.export_url_csv = f'www.merkulio.site/export/{self.key}/xlsx'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.key}'
