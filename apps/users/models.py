from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"null": True, "blank": True}


class Users(AbstractUser):

    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    username = models.CharField(max_length=255, verbose_name="Никнейм пользователя")
    first_name = models.CharField(max_length=150, **NULLABLE, verbose_name="Имя пользователя")
    last_name = models.CharField(max_length=150, **NULLABLE, verbose_name="Фамилия пользователя")
    middle_name = models.CharField(max_length=150, **NULLABLE, verbose_name="Отчество пользователя")
    phone = models.CharField(max_length=50, **NULLABLE, verbose_name="Телефон")
    birthday = models.DateField(**NULLABLE, verbose_name="День рождения")
    avatar = models.ImageField(
        default="users/avatar/avatar_default.png", upload_to="users/avatar/", **NULLABLE, verbose_name="Аватарка"
    )

    token = models.CharField(max_length=120, **NULLABLE, verbose_name="Токен")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.username}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "_us_users"
        ordering = ["email"]
        unique_together = ["email", "username"]
        permissions = [
            ("set_user_deactivate", "Can deacticate Пользователь"),
            ("view_all_users", "Can view all Пользователь"),
        ]
