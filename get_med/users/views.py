from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.decorators.http import require_POST

from .forms import RegisterForm
from django.contrib.auth import logout

def home(request):
    return render(request, 'home.html')

@require_POST
def logout_view(request):
    logout(request)  # Выход из системы
    return redirect('home')  # Перенаправление на главную страницу

@login_required
def account(request):
    return render(request, 'account.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Логиним пользователя сразу после регистрации
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
