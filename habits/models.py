from django.db import models
from django.conf import settings
from .validators import (
    validate_reward_or_related_habit,
    validate_execution_time,
    validate_related_habit_is_pleasant,
    validate_pleasant_habit_no_reward_or_related,
    validate_frequency
)

class Habit(models.Model):
    # Периодичность по умолчанию ежедневная
    DAILY = 1
    WEEKLY = 7

    PERIODICITY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=255, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='связанная привычка')
    frequency = models.PositiveSmallIntegerField(choices=PERIODICITY_CHOICES, default=DAILY, verbose_name='периодичность', validators=[validate_frequency])
    reward = models.CharField(max_length=255, blank=True, verbose_name='вознаграждение')
    execution_time = models.PositiveSmallIntegerField(verbose_name='время выполнения в секундах', validators=[validate_execution_time])
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def clean(self):
        """Вызов всех валидаторов при сохранении модели"""
        validate_reward_or_related_habit(self)
        validate_related_habit_is_pleasant(self)
        validate_pleasant_habit_no_reward_or_related(self)

    def save(self, *args, **kwargs):
        """Переопределяем save для вызова full_clean (который вызывает clean)"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

