from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class UserModelTest(TestCase):
    def test_profile_creation(self):
        """Тест автоматического создания профиля при создании пользователя"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)

    def test_profile_str(self):
        """Тест строкового представления профиля"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(str(user.profile), 'профильtestuser')


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_jwt_authentication(self):
        """Тест JWT аутентификации"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_credentials(self):
        """Тест неверных учетных данных"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/auth/token/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)