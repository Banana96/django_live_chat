from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("live_chat.urls")),
    path("admin/", admin.site.urls),
]
