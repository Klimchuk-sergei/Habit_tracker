import os
import requests
from celery import shared_task
from habits.models import Habit
from django.utils import timezone
from datetime import datetime, timedelta


@shared_task
def test_celery():
    """тестовая задача Celery"""
    print("✅ Celery работает! Задача выполнена.")
    return "Celery task completed!"


@shared_task
def send_telegram_message(chat_id, message):
    """отправка сообщения через ТГ бота"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not set!")
        return "TELEGRAM_BOT_TOKEN not set!"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print(f"✅ Сообщение отправлено в чат {chat_id}!")
            return f"Сообщение в чат {chat_id}!"
        else:
            error_msg = f"❌ Ошибка отправки: {response.text}"
            print(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"❌ Ошибка: {e}"
        print(error_msg)
        return error_msg


@shared_task
def check_habits_reminders():  # ИСПРАВЛЕНО название
    """ проверяем привычки и отправляем напоминания """

    now = timezone.now()
    current_time = now.time()
    current_hour = current_time.hour
    current_minute = current_time.minute

    print(f"⏰ Проверяем привычки в {current_time}")

    habits_sent = 0
    # находим привычки которые нужно выполнить
    habits = Habit.objects.all()
    for habit in habits:
        habit_time = habit.time
        # Проверяем совпадение времени (с допуском ±5 минут)
        if (abs(habit_time.hour - current_hour) == 0 and
                abs(habit_time.minute - current_minute) <= 5):

            # проверяем пользователя на наличие ТГ ID
            if hasattr(habit.user, 'profile') and habit.user.profile.telegram_chat_id:
                chat_id = habit.user.profile.telegram_chat_id

                # создаем сообщение - ИСПРАВЛЕНО: habit.action вместо habits.action
                message = f"🔔 Напоминание о привычке!\n\n" \
                          f"💫 Действие: {habit.action}\n" \
                          f"📍 Место: {habit.place}\n" \
                          f"⏰ Время: {habit.time}\n" \
                          f"⏱️ Время на выполнение: {habit.execution_time} сек."

                if habit.reward:
                    message += f"\n🎁 Вознаграждение: {habit.reward}"
                if habit.related_habit:
                    message += f"\n🔗 Связанная привычка: {habit.related_habit.action}"

                # отправляем сообщение
                send_telegram_message.delay(chat_id, message)
                habits_sent += 1
                print(f"📤 Отправлено напоминание для {habit.user.username}: {habit.action}")

    print(f"✅ Проверка завершена. Отправлено напоминаний: {habits_sent}")
    return f"проверено {habits.count()} привычек, отправлено {habits_sent} напоминаний"