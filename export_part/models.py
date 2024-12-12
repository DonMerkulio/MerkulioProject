from django.db import models


class ExportField(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название поля")
    is_included = models.BooleanField(default=True, verbose_name="Включено в экспорт")

    class Meta:
        verbose_name = "Поле для экспорта"
        verbose_name_plural = "Поля для экспорта"

    def __str__(self):
        return self.name
