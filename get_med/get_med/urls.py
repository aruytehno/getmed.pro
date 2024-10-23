"""
URL configuration for get_med project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views
from django.contrib.auth import views as auth_views
from users.views import confirm_email
from users.views import edit_profile

urlpatterns = [
    path('admin/', admin.site.urls),  # URL для админки
    path('', views.home, name='home'),  # Главная страница
    path('account/', views.account_view, name='account'),  # Личный кабинет пользователя
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.login_view, name='login'),  # Вход
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Выход
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('confirm-email/<uidb64>/<token>/', confirm_email, name='confirm_email'),
]
