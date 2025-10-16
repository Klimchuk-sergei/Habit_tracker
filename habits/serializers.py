from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    """Создание и обновление привычек"""
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',) # пользователь устанавливается автоматически

class HabitListSerializer(serializers.ModelSerializer):
    """Список привычек"""
    class Meta:
        model = Habit
        field = ('id', 'place', 'time', 'action', 'frequency', 'is_pleasant', 'is_public')

class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор публичных привычек"""
    class Meta:
        model = Habit
        field = ('id', 'place', 'time', 'action', 'frequency')
