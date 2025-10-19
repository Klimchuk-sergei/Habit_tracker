from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка схемы для документации
schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="API для трекера привычек. Создавайте полезные привычки и получайте напоминания в Telegram!",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@habittracker.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/habits/", include("habits.urls")),
    path("api/auth/", include("users.urls")),
    # Документация
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Документация API (альтернативный вариант)
    path("api/docs/", schema_view.with_ui("redoc", cache_timeout=0), name="api-docs"),
]
