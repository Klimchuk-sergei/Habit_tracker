import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = settings.TIME_ZONE
app.autodiscover_tasks()

# Добавляем периодические задачи
app.conf.beat_schedule = {
    'check-habits-every-minute': {
        'task': 'bot.tasks.check_habits_reminders',
        'schedule': 60.0,  # каждую минуту
    },
    'test-celery-every-5-minutes': {
        'task': 'bot.tasks.test_celery',
        'schedule': 300.0,  # каждые 5 минут
    },
}