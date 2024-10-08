from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def home(request):
    return render(request, 'home.html')

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
