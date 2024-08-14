from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.diary.urls", namespace="diary")),
    path("users/", include("apps.users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
