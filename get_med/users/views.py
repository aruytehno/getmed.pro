from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_POST
from .forms import UserRegistrationForm, ProfileEditForm
from django.contrib.auth import logout
from django.contrib import messages  # Для вывода сообщений
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

def home(request):
    """Главная страница."""
    return render(request, 'home.html')

@require_POST
def logout_view(request):
    """Выход из системы."""
    logout(request)  # Выход из системы
    return redirect('home')  # Перенаправление на главную страницу

@login_required
def account(request):
    """Личный кабинет пользователя."""
    return render(request, 'account.html')

def register(request):
    """Регистрация нового пользователя."""

    # Если пользователь уже аутентифицирован, перенаправляем на главную страницу
    if request.user.is_authenticated:
        return redirect('home')

    # Создаем форму с данными из POST-запроса
    form = UserRegistrationForm(request.POST or None)

    # Обрабатываем POST запрос с регистрацией
    if request.method == 'POST':
        # Если форма валидна, сохраняем пользователя и логиним его
        if form.is_valid():
            user = form.save()
            login(request, user)  # Логиним пользователя
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('home')
        # Если форма не валидна, выводим ошибки на фронт
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    # Отображаем форму на странице
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после успешного входа
        else:
            error_message = "Неверные учетные данные."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        if request.user.is_authenticated:
            return redirect('home')  # Перенаправление, если пользователь уже авторизован
        return render(request, 'login.html')


@login_required
def edit_profile(request):
    # Получаем или создаем профиль для текущего пользователя
    profile, created = Profile.objects.get_or_create(user=request.user)

    if created:
        messages.info(request, 'Профиль был создан, так как его ранее не существовало.')

    if request.method == 'POST':
        # Передаем профиль в форму для редактирования
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            # Сохраняем изменения в профиле и пользователе
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.save()

            form.save()
            messages.success(request, 'Изменения профиля успешно сохранены.')
            return redirect('account')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        # Инициализируем форму текущими данными пользователя и профиля
        form = ProfileEditForm(instance=profile, initial={
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
        })

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def account_view(request):
    # Пытаемся получить профиль пользователя
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Если профиль не существует, перенаправляем пользователя на страницу создания профиля
        messages.warning(request, 'Ваш профиль отсутствует. Пожалуйста, создайте его.')
        return redirect('edit_profile')

    # Передаем в контекст данные профиля и пользователя
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'account.html', context)


