from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from .tasks import send_telegram_message, check_habits_reminders
from habits.models import Habit


class TelegramTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Устанавливаем telegram_chat_id
        self.user.profile.telegram_chat_id = "123456789"
        self.user.profile.save()

        # Создаем привычку с текущим временем
        from django.utils import timezone
        now = timezone.now()
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=now.time(),  # Текущее время
            action="Тестовая привычка",
            is_pleasant=False,
            frequency=1,
            execution_time=120,
            is_public=True
        )

    @patch('bot.tasks.requests.post')
    def test_send_telegram_message_success(self, mock_post):
        """Тест успешной отправки сообщения в Telegram"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = send_telegram_message("123456789", "Тестовое сообщение")

        self.assertTrue(mock_post.called)
        self.assertIn("Сообщение в чат 123456789", result)

    @patch('bot.tasks.requests.post')
    def test_send_telegram_message_failure(self, mock_post):
        """Тест неудачной отправки сообщения в Telegram"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Error"
        mock_post.return_value = mock_response

        result = send_telegram_message("123456789", "Тестовое сообщение")

        self.assertTrue(mock_post.called)
        self.assertIn("Ошибка отправки", result)

    @patch('bot.tasks.send_telegram_message.delay')
    def test_check_habits_reminders(self, mock_send):
        """Тест проверки привычек и отправки напоминаний"""
        result = check_habits_reminders()

        # Проверяем что задача была вызвана
        self.assertTrue(mock_send.called)
        self.assertIn("проверено", result)

    @patch('bot.tasks.os.getenv')
    def test_send_telegram_message_no_token(self, mock_getenv):
        """Тест отправки сообщения без токена"""
        mock_getenv.return_value = None  # Нет токена

        result = send_telegram_message("123456789", "Тестовое сообщение")

        self.assertIn("TELEGRAM_BOT_TOKEN not set", result)


class CeleryTasksTest(TestCase):
    def test_test_celery_task(self):
        """Тест простой Celery задачи"""
        from .tasks import test_celery
        result = test_celery()
        self.assertEqual(result, "Celery task completed!")
