from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """профиль пользователя с доп полями"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    telegram_chat_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='ID чата в ТГ'
    )

    def __str__(self):
        return f'профиль{self.user.username}'

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


