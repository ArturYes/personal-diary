from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from apps.diary.forms import DiaryEntryForm
from apps.diary.models import DiaryEntry


class HomeView(TemplateView):
    template_name = "diary/home.html"
    extra_context = {"title": "Главная страница"}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class DiaryEntryListView(ListView):
    model = DiaryEntry
    template_name = "diary/diary_entry/diary_entry_list.html"
    extra_context = {"title": "Мой дневник"}

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        if user.is_superuser:
            return queryset
        else:
            queryset = queryset.filter(author=self.request.user)

            query = self.request.GET.get("q")
            if query:
                queryset = queryset.filter(Q(title__icontains=query) | Q(text__icontains=query))
            return queryset


class DiaryEntryDetailView(DetailView):
    model = DiaryEntry
    template_name = "diary/diary_entry/diary_entry_detail.html"
    extra_context = {"title": "Моя запись"}

    def get_object(self, *args, **kwargs):
        object = super().get_object()
        user = self.request.user
        if user.is_superuser or object.author == user:
            return object
        else:
            raise PermissionDenied


class DiaryEntryCreateView(LoginRequiredMixin, CreateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = "diary/diary_entry/diary_entry_form.html"
    extra_context = {"title": "Создать запис"}
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse("diary:diary_entry_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class DiaryEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = "diary/diary_entry/diary_entry_form.html"
    extra_context = {"title": "Редактировать запись"}
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse("diary:diary_entry_detail", kwargs={"pk": self.object.pk})

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or object.author == user:
            return object
        else:
            raise PermissionDenied


class DiaryEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = DiaryEntry
    template_name = "diary/diary_entry/diary_entry_form.html"
    extra_context = {"title": "Удаление статьи"}
    success_url = reverse_lazy("diary:diary_entry_list")
    login_url = reverse_lazy("users:login")

    def get_object(self, *args, **kwargs):
        object = super().get_object()
        user = self.request.user
        if user.is_superuser or object.author == user:
            return object
        else:
            raise PermissionDenied
