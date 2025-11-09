from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitViewSet

router = DefaultRouter()
router.register(r"my-habits", HabitViewSet, basename="my-habits")
router.register(r"public-habits", PublicHabitViewSet, basename="public-habits")

urlpatterns = [
    path("", include(router.urls)),
]
