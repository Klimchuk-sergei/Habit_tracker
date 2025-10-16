from django.shortcuts import render
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer, HabitListSerializer, PublicHabitSerializer


class IsOwner(permissions.BasePermission):
    """ Permission для проверки пользователя на владельца """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class HabitViewSet(viewsets.ModelViewSet):
    """ Views для привычек текущего пользователя """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner, ]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        # Для спискка используем простой сериализатор
        if self.action == 'list':
            return HabitListSerializer
        return HabitSerializer

    def perform_create(self, serializer):
        # устанавливаем текущего пользователя как владельца автоматически
        serializer.save(user=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """ Views для публичных привычек """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = PublicHabitSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]
