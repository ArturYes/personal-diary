from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Command(BaseCommand):
    help = "Создать суперпользователя с email, username и password"

    def handle(self, *args, **kwargs):
        email = input("Введите email: ")
        username = input("Введите username: ")
        password1 = input("Введите пароль: ")
        password2 = input("Подтвердите пароль: ")

        if password1 != password2:
            self.stderr.write(self.style.ERROR("Пароли не совпадают."))
            return

        try:
            user = User.objects.create_superuser(email=email, username=username, password=password1)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь "{username}" успешно создан.'))
        except ValidationError as e:
            self.stderr.write(self.style.ERROR(f"Ошибка: {e.message_dict}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка: {e}"))
