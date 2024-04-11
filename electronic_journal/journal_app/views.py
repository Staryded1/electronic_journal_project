from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout


def home(request):
    return render(request, 'home.html')

def registration(request):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Пытаемся создать нового пользователя
            user = User.objects.create_user(username=username, password=password, last_name=last_name, first_name=first_name)
            
            # Добавляем пользователя в группу "student"
            student_group = Group.objects.get(name='student')
            user.groups.add(student_group)

            # Проверяем учетные данные пользователя и авторизуем его
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Устанавливаем атрибут user объекту запроса, чтобы указать, что пользователь авторизован
                request.user = user
                # Перенаправляем пользователя на страницу после успешной регистрации
                return redirect('home')
            else:
                # Если пользователь не был авторизован, обрабатываем эту ситуацию
                # Например, вы можете показать сообщение об ошибке или перенаправить обратно на страницу регистрации с сообщением
                return render(request, 'registration.html', {'error_message': 'Ошибка при авторизации'})
        except IntegrityError:
            # Если пользователь с таким именем пользователя уже существует, обрабатываем эту ситуацию
            # Например, вы можете показать сообщение об ошибке или перенаправить обратно на страницу регистрации с сообщением
            return render(request, 'registration.html', {'error_message': 'Пользователь с таким именем уже существует'})

    # Если запрос GET, отображаем страницу регистрации
    return render(request, 'registration.html')

def login(request):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Если пользователь существует и введенный пароль верный, выполняем вход
            auth_login(request, user)
            # Перенаправляем пользователя на страницу dashboard
            return redirect('dashboard')
        else:
            # Если пользователь не найден или пароль неверен, показываем ошибку входа
            return render(request, 'login.html', {'error_message': 'Неверное имя пользователя или пароль.'})

    # Если запрос GET, показываем страницу входа
    return render(request, 'login.html')

def dashboard(request):
    # В этой функции мы будем обрабатывать запрос для страницы dashboard
    return render(request, 'dashboard.html')  # Пока просто отобразим шаблон dashboard.html

def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправляем пользователя на главную страницу