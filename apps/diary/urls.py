from django.urls import path

from apps.diary.apps import DiaryConfig
from apps.diary.views import (
    HomeView,
    DiaryEntryListView,
    DiaryEntryDetailView,
    DiaryEntryCreateView,
    DiaryEntryDeleteView,
    DiaryEntryUpdateView,
)

app_name = DiaryConfig.name


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("diary/", DiaryEntryListView.as_view(), name="diary_entry_list"),
    path("diary/create/", DiaryEntryCreateView.as_view(), name="diary_entry_create"),
    path("diary/<int:pk>/", DiaryEntryDetailView.as_view(), name="diary_entry_detail"),
    path("diary/update/<int:pk>/", DiaryEntryUpdateView.as_view(), name="diary_entry_update"),
    path("diary/delete/<int:pk>/", DiaryEntryDeleteView.as_view(), name="diary_entry_delete"),
]


