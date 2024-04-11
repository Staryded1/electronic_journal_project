from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    return render(request, 'home.html')

def registration(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, password=password, last_name=last_name, first_name=first_name)
            
            # Определяем роль пользователя как студента и добавляем его в соответствующую группу
            student_group = Group.objects.get_or_create(name='student')[0]
            user.groups.add(student_group)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                return render(request, 'registration.html', {'error_message': 'Ошибка при авторизации'})
        except IntegrityError:
            return render(request, 'registration.html', {'error_message': 'Пользователь с таким именем уже существует'})

    return render(request, 'registration.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error_message': 'Неверное имя пользователя или пароль.'})

    return render(request, 'login.html')

@login_required
def dashboard(request):
    is_teacher = request.user.groups.filter(name='teacher').exists()
    is_admin = request.user.groups.filter(name='admin').exists()
    return render(request, 'dashboard.html', {'is_teacher': is_teacher, 'is_admin': is_admin})

def grades(request):
    return render(request, 'grades.html')

def settings(request):
    return render(request, 'settings.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def mark(request):
    is_teacher = request.user.groups.filter(name='teacher').exists()
    is_admin = request.user.groups.filter(name='admin').exists()
    if request.user.is_authenticated and (is_teacher or is_admin):
        return render(request, 'mark.html', {'is_teacher': is_teacher, 'is_admin': is_admin})
    else:
        return HttpResponseForbidden("Доступ запрещен")