from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Habit
from .validators import validate_execution_time, validate_frequency
from django.core.exceptions import ValidationError


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Диван",
            time="21:00:00",
            action="Слушать музыку",
            is_pleasant=True,
            frequency=1,
            execution_time=120,
            is_public=True,
        )

    def test_habit_creation(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Читать книгу",
            is_pleasant=False,
            frequency=1,
            execution_time=120,
            is_public=True,
            related_habit=self.pleasant_habit,
        )
        self.assertEqual(habit.action, "Читать книгу")
        self.assertEqual(habit.user.username, "testuser")
        self.assertEqual(
            str(habit), f"Я буду {habit.action} в {habit.time} в {habit.place}"
        )

    def test_habit_with_reward(self):
        """Тест привычки с вознаграждением"""
        habit = Habit.objects.create(
            user=self.user,
            place="Кухня",
            time="08:00:00",
            action="Пить воду",
            is_pleasant=False,
            frequency=1,
            execution_time=60,
            is_public=False,
            reward="Выпить кофе",
        )
        self.assertEqual(habit.reward, "Выпить кофе")


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Тестовая привычка",
            is_pleasant=False,
            frequency=1,
            execution_time=120,
            is_public=True,
        )

        self.private_habit = Habit.objects.create(
            user=self.user,
            place="Спальня",
            time="22:00:00",
            action="Приватная привычка",
            is_pleasant=False,
            frequency=1,
            execution_time=90,
            is_public=False,
        )

    def test_get_habits_list(self):
        """Тест получения списка привычек"""
        response = self.client.get("/api/habits/my-habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["count"], 2)

    def test_create_habit(self):
        """Тест создания привычки через API"""
        data = {
            "place": "Парк",
            "time": "09:00:00",
            "action": "Гулять",
            "is_pleasant": False,
            "frequency": 1,
            "execution_time": 120,
            "is_public": True,
        }
        response = self.client.post("/api/habits/my-habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(response.data["action"], "Гулять")

    def test_get_habit_detail(self):
        """Тест получения деталей привычки"""
        response = self.client.get(f"/api/habits/my-habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Тестовая привычка")

    def test_update_habit(self):
        """Тест обновления привычки"""
        data = {
            "place": "Библиотека",
            "time": "19:00:00",
            "action": "Читать",
            "is_pleasant": False,
            "frequency": 1,
            "execution_time": 120,
            "is_public": True,
        }
        response = self.client.put(f"/api/habits/my-habits/{self.habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, "Библиотека")

    def test_delete_habit(self):
        """Тест удаления привычки"""
        response = self.client.delete(f"/api/habits/my-habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)

    def test_public_habits_access(self):
        """Тест доступа к публичным привычкам"""
        response = self.client.get("/api/habits/public-habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем что все возвращенные привычки публичные
        if response.data["results"]:
            for habit in response.data["results"]:
                self.assertTrue(habit.get("is_public", False))

    def test_other_user_cannot_access_private_habits(self):
        """Тест что другой пользователь не видит приватные привычки"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get("/api/habits/my-habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)


class HabitValidatorTest(TestCase):
    def test_execution_time_validation_valid(self):
        """Тест валидации времени выполнения (валидное значение)"""
        try:
            validate_execution_time(120)
        except ValidationError:
            self.fail("validate_execution_time raised ValidationError unexpectedly!")

    def test_execution_time_validation_invalid(self):
        """Тест валидации времени выполнения (невалидное значение)"""
        with self.assertRaises(ValidationError):
            validate_execution_time(121)

    def test_frequency_validation_valid(self):
        """Тест валидации периодичности (валидное значение)"""
        try:
            validate_frequency(7)
        except ValidationError:
            self.fail("validate_frequency raised ValidationError unexpectedly!")

    def test_frequency_validation_invalid(self):
        """Тест валидации периодичности (невалидное значение)"""
        with self.assertRaises(ValidationError):
            validate_frequency(8)


class PermissionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Тестовая привычка",
            is_pleasant=False,
            frequency=1,
            execution_time=120,
            is_public=False,
        )

    def test_owner_can_access(self):
        """Тест что владелец может доступть свою привычку"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/habits/my-habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_access(self):
        """Тест что другой пользователь не может доступть чужую привычку"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(f"/api/habits/my-habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HabitValidatorIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Диван",
            time="21:00:00",
            action="Слушать музыку",
            is_pleasant=True,
            frequency=1,
            execution_time=120,
            is_public=True,
        )

    def test_pleasant_habit_cannot_have_reward(self):
        """Тест что приятная привычка не может иметь вознаграждение"""
        habit = Habit(
            user=self.user,
            place="Кровать",
            time="23:00:00",
            action="Расслабляться",
            is_pleasant=True,
            frequency=1,
            execution_time=120,
            is_public=False,
            reward="Что-то",  # Не должно быть у приятной привычки
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_cannot_have_both_reward_and_related(self):
        """Тест что привычка не может иметь и вознаграждение и связанную привычку"""
        habit = Habit(
            user=self.user,
            place="Офис",
            time="15:00:00",
            action="Работать",
            is_pleasant=False,
            frequency=1,
            execution_time=120,
            is_public=True,
            reward="Отдохнуть",
            related_habit=self.pleasant_habit,  # Нельзя одновременно с reward
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_must_be_pleasant(self):
        """Тест что связанная привычка должна быть приятной"""
        # Создаем НЕприятную привычку
        not_pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Спортзал",
            time="19:00:00",
            action="Тренироваться",
            is_pleasant=False,
            frequency=1,
            execution_time=120,
            is_public=True,
        )

        habit = Habit(
            user=self.user,
            place="Дом",
            time="20:00:00",
            action="Читать",
            is_pleasant=False,
            frequency=1,
            execution_time=120,
            is_public=True,
            related_habit=not_pleasant_habit,  # Ошибка - не приятная привычка
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()


class PaginationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем больше 5 привычек для тестирования пагинации
        for i in range(7):
            Habit.objects.create(
                user=self.user,
                place=f"Место {i}",
                time="20:00:00",
                action=f"Привычка {i}",
                is_pleasant=False,
                frequency=1,
                execution_time=120,
                is_public=True,
            )

    def test_pagination(self):
        """Тест пагинации (5 привычек на страницу)"""
        response = self.client.get("/api/habits/my-habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)  # Первая страница
        self.assertEqual(response.data["count"], 7)  # Всего привычек
        self.assertIsNotNone(
            response.data.get("next")
        )  # Должна быть следующая страница

    def test_second_page(self):
        """Тест второй страницы пагинации"""
        response = self.client.get("/api/habits/my-habits/?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Оставшиеся 2 привычки


class ValidatorEdgeCasesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_pleasant_habit_with_related_habit(self):
        """Тест что приятная привычка не может иметь связанную привычку"""
        pleasant_habit1 = Habit(
            user=self.user,
            place="Диван",
            time="21:00:00",
            action="Слушать музыку",
            is_pleasant=True,
            frequency=1,
            execution_time=120,
            is_public=True,
        )
        pleasant_habit1.save()

        pleasant_habit2 = Habit(
            user=self.user,
            place="Кровать",
            time="22:00:00",
            action="Расслабляться",
            is_pleasant=True,
            frequency=1,
            execution_time=120,
            is_public=False,
            related_habit=pleasant_habit1,  # Ошибка - приятная привычка не может иметь связанную
        )
        with self.assertRaises(ValidationError):
            pleasant_habit2.full_clean()

    def test_min_frequency_validation(self):
        """Тест минимальной периодичности"""
        with self.assertRaises(ValidationError):
            validate_frequency(0)

    def test_max_frequency_validation(self):
        """Тест максимальной периодичности"""
        with self.assertRaises(ValidationError):
            validate_frequency(8)
