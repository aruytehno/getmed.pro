from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  # Убедитесь, что у вас есть модель Profile
from django.contrib.auth import get_user_model
from django.forms.widgets import DateInput

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
    birth_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),  # Виджет с типом "date"
        required=False,
        input_formats=['%Y-%m-%d']  # Указываем формат даты
    )

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


