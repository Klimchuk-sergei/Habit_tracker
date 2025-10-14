from django.db import models
from django.conf import settings

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
    frequency = models.PositiveSmallIntegerField(choices=PERIODICITY_CHOICES, default=DAILY, verbose_name='периодичность')
    reward = models.CharField(max_length=255, blank=True, verbose_name='вознаграждение')
    execution_time = models.PositiveSmallIntegerField(verbose_name='время выполнения в секундах')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

