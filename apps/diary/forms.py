from django.forms import ModelForm
from core.forms import StyleFormMixin
from apps.diary.models import DiaryEntry


class DiaryEntryForm(StyleFormMixin, ModelForm):

    class Meta:
        model = DiaryEntry
        fields = ("title", "text", "image", "is_published")
