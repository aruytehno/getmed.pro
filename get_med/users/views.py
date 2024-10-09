from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_POST
from .forms import RegisterForm, ProfileEditForm
from django.contrib.auth import logout

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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после успешной регистрации
    else:
        if request.user.is_authenticated:
            return redirect('home')  # Перенаправление, если пользователь уже авторизован
        form = RegisterForm()
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
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('account')  # Перенаправляем на страницу аккаунта
    else:
        form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit_profile.html', {'form': form})


@login_required
def account_view(request):
    profile = request.user.profile  # Получаем профиль пользователя
    context = {
        'profile': profile,  # Передаём профиль в контекст
    }
    return render(request, 'account.html', context)  # Предполагая, что ваш шаблон называется account.html