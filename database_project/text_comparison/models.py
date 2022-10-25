from django.db import models
from django.contrib.auth.models import User
import uuid


class UserComparisons(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    comparison_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID камеры',
        unique=True,
    )
    text = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    nearest_text = models.CharField(
        max_length=255,
        verbose_name='Ближайшее название',
    )
    similarity = models.FloatField(
        verbose_name='Похожесть',
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    def __str__(self):
        return f"Сравнение пользователя {self.user.username}"

    class Meta:
        verbose_name = 'Сравнение'
        verbose_name_plural = 'Сравнения'
