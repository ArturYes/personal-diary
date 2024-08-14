from django.db import models

from apps.users.models import NULLABLE, Users


class DiaryEntry(models.Model):
    """Модель записи пользователя в его дневнике."""

    author = models.ForeignKey(Users, on_delete=models.CASCADE, **NULLABLE, verbose_name="Автор")

    title = models.CharField(max_length=255, verbose_name="Название записи")
    text = models.TextField(verbose_name="Текст записи")
    image = models.ImageField(
        upload_to="diary/diary_entry", default="diary/diary_entry/default.png", **NULLABLE, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    is_published = models.BooleanField(default=True, verbose_name="Статус публикации")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["author", "updated_at"]
        db_table = "_d_diary_entry"
        db_table_comment = "Записи в дневнике"
