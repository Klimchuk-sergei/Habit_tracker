from django.core.exceptions import ValidationError

def validate_reward_or_related_habit(value):
    """ Исключаем одновременный выбор связанной привычки и указания вознаграждения. """
    from habits.models import Habit # импортирую здесь, для исключения циклического импорта.import

    if value.reward and value.related_habit:
        raise ValidationError(
            'нельзя выбирать одновременно связанную привычку и вознаграждение',
            code='invalid_reward_and_related_habit',
        )

def validate_execution_time(value):
    """ время на вполнение не более 120 секунд """
    if value > 120:
        raise ValidationError(
            'время на выполнение не должно превышать 120 секунд',
            code='invalid_execution_time',
        )

def validate_related_habit_is_pleasant(value):
    """ связаной привычкой, может быть только приятная привычка """
    if value and not value.is_pleasant:
        raise ValidationError(
            'в связаные привчки можно добавить только приятные привычки ',
            code='invalid_related_habit_is_pleasant'
        )

def validate_pleasant_habit_no_reward_or_related(value):
    """ для приятной привычки не может быть вознаграждения или связанной привычки """
    if value.is_pleasant and (value.reward or value.related_habit):
        raise ValidationError(
            'для приятной привычки не может быть вознаграждения или связанной привычки',
            code='invalid_pleasant_habit_no_reward_or_related'
        )

def validate_frequency(value):
    """Нельзя выполнять привычку реже, чем 1 ра в 7 дней"""
    if value < 1 or value > 7:
        raise ValidationError(
            'период выполнения привычки должен быть от 1 до 7 дней',
            code='invalid_frequency'
        )

