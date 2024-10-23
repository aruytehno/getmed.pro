from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    USER_ROLES = [
        ('doctor', 'Доктор'),
        ('patient', 'Пациент'),
    ]

    # Связь с моделью User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Дополнительные поля профиля
    role = models.CharField(max_length=7, choices=USER_ROLES, default='patient')
    middle_name = models.CharField(max_length=30, blank=True, default='')
    gender = models.CharField(max_length=6, choices=[('male', 'Мужской'), ('female', 'Женский')], blank=True, default='')
    birth_date = models.DateField(null=True, blank=True)
    new_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    def get_full_name(self):
        """Возвращает полное имя пользователя с учетом отчества"""
        full_name = f"{self.user.first_name} {self.middle_name} {self.user.last_name}".strip()
        return ' '.join(full_name.split())  # Удаление лишних пробелов

    def get_gender_display(self):
        """Возвращает пол на русском языке"""
        if self.gender == 'male':
            return 'Мужской'
        elif self.gender == 'female':
            return 'Женский'
        return 'Не указан'


# Сигналы для создания и сохранения профиля пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создать профиль пользователя при создании нового пользователя."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранить профиль пользователя при обновлении пользователя."""
    instance.profile.save()
