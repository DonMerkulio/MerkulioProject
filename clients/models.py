from django.db import models


class Clients(models.Model):
    class Meta:
        verbose_name = 'Клиента'
        verbose_name_plural = 'Клиенты'

    name = models.CharField(verbose_name='Имя', max_length=255)
    url = models.CharField(verbose_name='Ссылка на магазин', max_length=255)
    key = models.CharField(verbose_name='Ключ', max_length=10, unique=True, blank=True)
    export_url = models.CharField(verbose_name='Ссылка для клиента', max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.export_url:  # Генерировать ключ только если его нет
            self.export_url = f'http://194.58.120.165:8000/export/{self.key}/'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.key}'
