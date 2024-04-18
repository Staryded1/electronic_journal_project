from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .forms import SpecialtyForm  # Импорт вашей формы для специальностей
from .models import Specialty  # Импорт вашей модели для специальностей
from django.contrib.admin.views.decorators import staff_member_required
from .forms import GroupForm, StudentForm
import random
import string
import pandas as pd
from .models import Student



def home(request):
    return render(request, 'home.html')

def registration(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')  
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name)
            
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
            if user.is_staff:  # Проверяем, является ли пользователь администратором
                return redirect('admin_panel')  # Перенаправляем на страницу администратора
            else:
                return redirect('dashboard')  # Перенаправляем на страницу dashboard для обычных пользователей
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

@login_required
def settings(request):
    if request.method == 'POST':
        # Обработка POST-запроса при отправке формы
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Сохранение изменений в профиле пользователя
        user = request.user
        if email:  # Проверяем, был ли предоставлен email
            user.email = email
            user.save()
            messages.success(request, 'Настройки профиля успешно сохранены.')
            return redirect(reverse('settings'))
        
    # Проверка, является ли пользователь преподавателем или администратором
    is_teacher = request.user.groups.filter(name='teacher').exists()
    is_admin = request.user.groups.filter(name='admin').exists()
    
    # Отображение страницы настроек
    return render(request, 'settings.html', {'user': request.user, 'is_teacher': is_teacher, 'is_admin': is_admin})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def mark(request):
    is_teacher = request.user.groups.filter(name='teacher').exists()
    is_admin = request.user.groups.filter(name='admin').exists()
    
    if request.method == 'POST':
        # Process the form submission here if needed
        # Then redirect to the department selection page
        return redirect(reverse('department_selection'))
    
    if request.user.is_authenticated and (is_teacher or is_admin):
        return render(request, 'mark.html', {'is_teacher': is_teacher, 'is_admin': is_admin})
    else:
        return HttpResponseForbidden("Доступ запрещен")

@login_required
def department_selection(request):
    is_teacher = request.user.groups.filter(name='teacher').exists()
    is_admin = request.user.groups.filter(name='admin').exists()
    
    # Обработка POST-запроса
    if request.method == 'POST':
        # Здесь вы можете получить выбранное отделение из запроса и выполнить необходимые действия с ним
        pass

    # Отображение страницы выбора отделения
    return render(request, 'department_selection.html', {'is_teacher': is_teacher, 'is_admin': is_admin})



@staff_member_required
def admin_panel(request):
    return render(request, 'admin_panel.html')

def add_specialty(request):
    form = SpecialtyForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Специальность успешно добавлена.')
            return redirect(request.path)  # Оставляем пользователя на той же странице
    return render(request, 'add_specialty.html', {'form': form})

def add_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем данные формы в базу данных
            # Добавляем сообщение об успешном добавлении группы
            messages.success(request, 'Группа успешно добавлена.')
            return redirect('add_group')  # Перенаправляем на страницу добавления группы
    else:
        form = GroupForm()  # Создаем пустую форму

    # Получаем список специальностей для передачи в шаблон
    specialties = Specialty.objects.all()

    return render(request, 'add_group.html', {'form': form, 'specialties': specialties})



def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # Генерация логина и пароля и добавление их к студенту
            student.login = generate_login(student.first_name, student.last_name)
            student.password = generate_password()
            student.save()
            messages.success(request, 'Студент успешно добавлен.')
            return redirect('add_student')
    else:
        form = StudentForm()

    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        try:
            # Чтение файла Excel с помощью Pandas
            df = pd.read_excel(excel_file)
            
            # Обработка данных и добавление студентов
            for index, row in df.iterrows():
                student = Student(
                    last_name=row['Фамилия'],
                    first_name=row['Имя'],
                    middle_name=row.get('Отчество', None),  # Отчество необязательное поле
                    birth_year=row['Год рождения'],
                    login=generate_login(row['Имя'], row['Фамилия']),
                    password=generate_password()
                )
                student.save()
            
            messages.success(request, 'Студенты успешно добавлены.')
            return redirect('add_student')
        except Exception as e:
            messages.error(request, f'Ошибка при обработке файла: {e}')

    return render(request, 'add_student.html', {'form': form})

def generate_login(first_name, last_name):
    # Генерация логина на основе имени и фамилии
    return (first_name[0] + last_name).lower()

def generate_password():
    # Генерация случайного пароля средней сложности
    # Пароль будет содержать буквы верхнего и нижнего регистра, цифры и специальные символы
    password_length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(password_length))
    return password