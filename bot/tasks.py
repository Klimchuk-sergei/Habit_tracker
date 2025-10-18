import os

import requests
from celery import shared_task


@shared_task
def test_celery():
    """тестовая задача Celery"""
    print("Celery работает! Задача выполнена.")
    return "Celery task completed!"


@shared_task
def send_telegram_message(chat_id, message):
    """отправка сообщения через ТГ бота"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        return "TELEGRAM_BOT_TOKEN not set!"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return f"Сообщение в чат {chat_id}!"
        else:
            return f"Ошибка отправки: {response.text}"
    except Exception as e:
        return f"Ошибка: {e}"
