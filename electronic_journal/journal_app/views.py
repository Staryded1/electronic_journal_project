from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'home.html')

def registration(request):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Создаем нового пользователя
        user = User.objects.create_user(username=username, password=password, last_name=last_name, first_name=first_name)
        
        # Автоматически входим в систему после регистрации
        login(request, user)

        # Перенаправляем пользователя на страницу входа
        return redirect('login')

    # Если запрос GET, отображаем страницу регистрации
    return render(request, 'registration.html')

def login(request):
    return render(request, 'login.html')
