from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  # Убедитесь, что у вас есть модель Profile
from django.contrib.auth import get_user_model
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError
from datetime import date

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    email = forms.EmailField(required=True, label="Электронная почта")  # Добавляем поле для email
    role = forms.ChoiceField(choices=[('doctor', 'Доктор'), ('patient', 'Пациент')], label="Роль")  # Поле для выбора роли

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']  # Добавляем 'role' в список полей

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже используется.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Создаем профиль пользователя с выбранной ролью
            profile = Profile(user=user, role=self.cleaned_data['role'])
            profile.save()
        return user


class ProfileEditForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        label="Дата рождения",
        required=True
    )

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = (today - birth_date).days // 365  # Рассчитываем возраст
            if age < 18:
                raise ValidationError("Возраст должен быть не менее 18 лет.")
            if age > 100:
                raise ValidationError("Возраст должен быть не более 100 лет.")
        return birth_date

    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')

    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'birth_date']


