from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import uuid


class UserCamera(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    camera_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID камеры',
        unique=True,
    )
    rtsp_address = models.CharField(
        max_length=256,
        verbose_name='RTSP адрес'
    )
    image = models.FileField(
        default='',
        upload_to='accounts/cameras',
        null=True,
        blank=True
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    def __str__(self):
        return f"Камера пользователя {self.user.username}"

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'


class UserSnapshot(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    camera = models.ForeignKey(
        UserCamera,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID изображения',
        unique=True,
    )
    image = models.FileField(
        default='',
        upload_to='accounts/images',
        null=True,
        blank=True
    )
    color = models.CharField(
        verbose_name='Цвет ТС',
        max_length=20
    )
    vehicle_type = models.CharField(
        verbose_name='Тип ТС',
        max_length=32
    )
    plate_number = models.CharField(
        verbose_name='Номер ТС',
        max_length=32
    )
    date = models.DateTimeField(
        verbose_name='Время фиксации'
    )

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Распознанное изображение'
        verbose_name_plural = 'Распознанные изображения'
