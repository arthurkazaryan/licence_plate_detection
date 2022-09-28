from django.db import models


# Create your models here.
class CameraData(models.Model):
    camera_id = models.PositiveIntegerField(
        verbose_name='ID камеры',
    )
    direction = models.CharField(
        verbose_name='Направление',
        max_length=20
    )
    color = models.CharField(
        verbose_name='Цвет ТС',
        max_length=20
    )
    vehicle_type = models.CharField(
        verbose_name='Тип ТС',
        max_length=20
    )
    number = models.CharField(
        verbose_name='Номер ТС',
        max_length=20
    )
    date = models.DateTimeField(
        verbose_name='Время фиксации'
    )

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = 'Фиксация ТС'
        verbose_name_plural = 'Фиксация ТС'
