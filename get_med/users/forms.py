from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  # Предполагается, что у вас есть модель Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Добавим поле для email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile  # Укажите свою модель, если у вас есть
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'email']

    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)