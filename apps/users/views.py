import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.users.forms import LoginForm, RecoveryForm, UserForm, UserRegisterForm
from apps.users.models import Users
from config.settings import EMAIL_HOST_USER
from core.services import make_random_password


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("users:profile")


class UserLogoutView(LogoutView):
    template_name = "users/login.html"


class UserRegisterView(CreateView):
    model = Users
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")
    extra_context = {"title": "Регистрация пользователя"}

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(15)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/confirm-email/{token}/"

        try:
            send_mail(
                subject="Подтверждение электронной почты!",
                message=f"Здравствуйте! "
                f"Для подтверждения регистрации на сайте 'My Personal Diary' перейдите по ссылке:"
                f"{url}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except Exception:
            print("Ошибка при отправке письма верификации")
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(Users, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect(reverse("users:login"))


class UserPasswordResetView(PasswordResetView):
    form_class = RecoveryForm
    template_name = "users/recovery_form.html"

    def form_valid(self, form):
        if self.request.method == "POST":
            user_email = self.request.POST["email"]
            user = Users.objects.filter(email=user_email).first()
            if user:
                password = make_random_password()
                user.set_password(password)
                user.save()
                try:
                    send_mail(
                        subject="Восстановление пароля на сайте",
                        message=f"Здравствуйте!\n"
                        f"Ваш пароль для доступа на сайт 'My Personal Diary' изменен:\n"
                        f"Данные для входа:\n"
                        f"Email: {user_email}\n"
                        f"Пароль: {password}",
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[user.email],
                    )
                except Exception as err:
                    print(err)
                    print(f"Ошибка при отправке пароля пользователю: ({user=}), на email: {user_email}")
            return HttpResponseRedirect(reverse("users:login"))
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    model = Users
    template_name = "users/profile.html"
    extra_context = {"title": "Профиль пользователя"}
    login_url = reverse_lazy("users:login")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UserForm
    template_name = "users/user_form.html"
    extra_context = {"title": "Редактирование пользователя"}
    login_url = reverse_lazy("users:login")
    success_url = "users:profile"

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user == obj:
            return obj
        else:
            raise PermissionDenied


@permission_required("users.set_user_deactivate")
def toggle_activity(request, pk):
    """Контроллер изменения статуса пользователя"""
    user = get_object_or_404(Users, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect(reverse("users:profile"))
