from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  # Убедитесь, что у вас есть модель Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    email = forms.EmailField(required=True)  # Добавляем поле для email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # password1 и password2 берутся из UserCreationForm

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже используется.")
        return email


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Profile  # Укажите свою модель, если у вас есть
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже зарегистрирован.")
        return email
