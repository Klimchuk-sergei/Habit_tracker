from django.core.exceptions import ValidationError


def validate_reward_or_related_habit(value):
    """Исключаем одновременный выбор связанной привычки и указания вознаграждения"""
    if value.reward and value.related_habit:
        raise ValidationError(
            "Нельзя одновременно выбирать связанную привычку и вознаграждение.",
            code="invalid_reward_and_related",
        )


def validate_execution_time(value):
    """Время выполнения должно быть не больше 120 секунд"""
    if value > 120:
        raise ValidationError(
            "Время выполнения не может превышать 120 секунд.",
            code="invalid_execution_time",
        )


def validate_related_habit_is_pleasant(value):
    """В связанные привычки могут попадать только привычки с признаком приятной привычки"""
    if value.related_habit and not value.related_habit.is_pleasant:
        raise ValidationError(
            "В связанные привычки можно добавлять только приятные привычки.",
            code="invalid_related_habit",
        )


def validate_pleasant_habit_no_reward_or_related(value):
    """У приятной привычки не может быть вознаграждения или связанной привычки"""
    if value.is_pleasant and (value.reward or value.related_habit):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки.",
            code="invalid_pleasant_habit",
        )


def validate_frequency(value):
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    if value < 1 or value > 7:
        raise ValidationError(
            "Периодичность выполнения привычки должна быть от 1 до 7 дней.",
            code="invalid_frequency",
        )
