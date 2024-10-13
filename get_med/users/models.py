from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    # Связь с моделью User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Дополнительные поля профиля
    middle_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Мужской'), ('female', 'Женский')], blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создать профиль пользователя при создании нового пользователя."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранить профиль пользователя при обновлении пользователя."""
    instance.profile.save()
