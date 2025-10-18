from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для Создание и обновление привычек"""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)  # пользователь устанавливается автоматически

    def validate_execution_time(self, value):
        """Валидация времени выполнения"""
        if value > 120:
            raise serializers.ValidationError("Время выполнения не может превышать 120 секунд.")
        return value


class HabitListSerializer(serializers.ModelSerializer):
    """Сериализатор для Список привычек"""

    class Meta:
        model = Habit
        fields = (
            "id",
            "place",
            "time",
            "action",
            "frequency",
            "is_pleasant",
            "is_public",
        )


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор публичных привычек(только чтение)"""

    class Meta:
        model = Habit
        fields = ("id", "place", "time", "action", "frequency")
