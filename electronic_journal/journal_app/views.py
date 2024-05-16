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
from .models import Specialty, Teacher  # Импорт вашей модели для специальностей
from django.contrib.admin.views.decorators import staff_member_required
from .forms import GroupForm, StudentForm
import random
import string
import pandas as pd
from .models import Student
import transliterate
from journal_app.models import Group
import re
from django.contrib.auth.models import Group as AuthGroup
from .forms import TeacherForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Discipline, Student, JournalEntry
from .forms import JournalCreationForm
from openpyxl import Workbook
from django.http import HttpResponse
from django.utils.encoding import force_str





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
    user = request.user

    if request.method == 'POST':
        # Обработка POST-запроса при отправке формы
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Сохранение изменений в профиле пользователя
        if first_name and last_name and email:  # Проверяем, были ли предоставлены все поля
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, 'Настройки профиля успешно сохранены.')
            return redirect(reverse('settings'))

    return render(request, 'settings.html', {'user': user})
        
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
    
    # Get specialties from the database
    specialties = Specialty.objects.all()
    
    # Обработка POST-запроса
    if request.method == 'POST':
        # Здесь вы можете получить выбранную специальность из запроса и выполнить необходимые действия с ней
        pass

    # Отображение страницы выбора специальности
    return render(request, 'department_selection.html', {'specialties': specialties, 'is_teacher': is_teacher, 'is_admin': is_admin})

def group_selection(request):
    is_teacher = request.user.groups.filter(name='teacher').exists()
    is_admin = request.user.groups.filter(name='admin').exists()
    selected_specialty_id = None
    groups = None
    
    if request.method == 'POST':
        selected_specialty_id = request.POST.get('specialty')  # Получаем идентификатор выбранной специальности из POST-запроса
        if selected_specialty_id:
            selected_specialty = get_object_or_404(Specialty, code=selected_specialty_id)  # Получаем объект выбранной специальности или 404, если не найден
            groups = selected_specialty.group_set.all()  # Получаем все группы, связанные с выбранной специальностью
    
    return render(request, 'group_selection.html', {'is_teacher': is_teacher, 'is_admin': is_admin, 'groups': groups})



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
    form = StudentForm()
    groups = Group.objects.all()  # Получаем список всех учебных групп из базы данных
    student_role_group, created = AuthGroup.objects.get_or_create(name='student')  # Получаем или создаем группу ролей "student"

    if request.method == 'POST':
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            group_id = request.POST.get('group_id')  # Получаем ID выбранной учебной группы
            try:
                group = Group.objects.get(pk=group_id)  # Получаем объект учебной группы по ID
                df = pd.read_excel(excel_file)
                added_students = 0
                for index, row in df.iterrows():
                    try:
                        login = generate_unique_login(row['Имя'], row['Фамилия'], group.name)
                        password = generate_password()

                        try:
                            user = User.objects.create_user(username=login, password=password)
                            user.groups.add(student_role_group)  # Добавляем пользователя в группу ролей "student"
                            student = Student.objects.create(
                                last_name=row['Фамилия'],
                                first_name=row['Имя'],
                                middle_name=row.get('Отчество', None),
                                birth_year=row['Год рождения'],
                                login=login,
                                password=password,
                                group=group,  # Привязываем студента к выбранной учебной группе
                                user=user  # Связываем объект Student с объектом User
                            )
                            added_students += 1
                        except IntegrityError:
                            messages.error(request, f'Ошибка при создании пользователя для {row["Имя"]} {row["Фамилия"]}. Логин уже существует.')
                    except Exception as e:
                        messages.error(request, f'Ошибка при обработке студента {row["Имя"]} {row["Фамилия"]}: {e}')
                messages.success(request, f'Студенты успешно добавлены: {added_students}')
                return redirect('add_student')
            except Exception as e:
                messages.error(request, f'Ошибка при обработке файла: {e}')
        else:
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                group_id = form.cleaned_data['group_id'].id  # Получаем ID выбранной учебной группы из формы
                group = Group.objects.get(pk=group_id)  # Получаем объект учебной группы по ID
                login = generate_unique_login(student.first_name, student.last_name, group.name)
                password = generate_password()

                # Создаем пользователя с сгенерированным логином и паролем
                try:
                    user = User.objects.create_user(username=login, password=password)
                    user.groups.add(student_role_group)  # Добавляем пользователя в группу ролей "student"
                    student.login = login
                    student.password = password
                    student.group = group  # Привязываем студента к выбранной учебной группе
                    student.user = user  # Связываем объект Student с объектом User
                    student.save()
                    messages.success(request, 'Студент успешно добавлен.')
                    return redirect('add_student')
                except IntegrityError:
                    messages.error(request, 'Ошибка при создании пользователя. Возможно, пользователь с таким логином уже существует.')

    return render(request, 'add_student.html', {'form': form, 'groups': groups})  # Передаем список групп в контекст




# Генерация логина на основе имени, фамилии и группы (в транслите)
def generate_unique_login(first_name, last_name, group_name):
    # Начальная длина частей имени и фамилии
    name_length = 1
    last_length = 1
    
    while True:
        try:
            # Проверяем длину частей имени и фамилии, увеличивая их по мере необходимости
            name_part = first_name[:name_length] if len(first_name) >= name_length else first_name
            last_part = last_name[:last_length] if len(last_name) >= last_length else last_name

            if name_length == len(first_name) and last_length == len(last_name):
                break

            # Увеличиваем длину частей имени и фамилии, чтобы избежать ошибок
            if len(name_part) == name_length:
                name_length += 1
            if len(last_part) == last_length:
                last_length += 1

            # Выполняем транслитерацию только если длина частей больше 1
            if len(name_part) > 1 and len(last_part) > 1:
                login_base = transliterate.translit(name_part + last_part, reversed=True).lower()
            else:
                login_base = (name_part + last_part).lower()

            login = f"{group_name}-{login_base}"

            if not User.objects.filter(username=login).exists():
                return login
        except Exception as e:
            # Если возникла ошибка транслитерации, увеличиваем длину частей имени и фамилии
            name_length += 1
            last_length += 1

def generate_password():
    # Генерация случайного пароля средней сложности
    # Пароль будет содержать буквы верхнего и нижнего регистра, цифры и специальные символы
    password_length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(password_length))
    return password


def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = generate_password()  # Генерируем пароль
            teacher_role_group, created = AuthGroup.objects.get_or_create(name='teacher')  # Получаем или создаем группу ролей "teacher"
            try:
                user = User.objects.create_user(username=email, email=email, password=password)  # Создаем пользователя с email в качестве логина
                teacher = Teacher.objects.create(
                    user=user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=email,
                    password=password  # Сохраняем пароль в модели Teacher без хеширования
                )
                user.groups.add(teacher_role_group)  # Добавляем пользователя в группу "teacher"
                messages.success(request, f'Преподаватель успешно добавлен. Логин: {email}, Пароль: {password}')
                return HttpResponseRedirect('/add_teacher/')  # Redirect to the add_teacher page
            except Exception as e:
                messages.error(request, f'Ошибка при добавлении преподавателя: {e}')
                return HttpResponseRedirect('/add_teacher/')  # Redirect to the add_teacher page with an error message
    else:
        form = TeacherForm()

    return render(request, 'add_teacher.html', {'form': form})


def generate_excel_journal(journal_entries):
    wb = Workbook()
    ws = wb.active
    ws.append(['Фамилия', 'Имя', 'Отчество', 'Дата', 'Оценка'])

    for entry in journal_entries:
        ws.append([entry.student.last_name, entry.student.first_name, entry.student.middle_name, entry.date, entry.mark])

    return wb

def create_journal(request):
    groups = Group.objects.all()  # Получаем список всех групп

    if request.method == 'POST':
        form = JournalCreationForm(request.POST)
        if form.is_valid():
            discipline = form.cleaned_data['discipline']
            date = form.cleaned_data['date']
            group_id = form.cleaned_data['group']  # Получаем ID выбранной группы
            group = get_object_or_404(Group, id=group_id)  # Получаем объект группы по ID
            students = group.student_set.all()  # Получаем всех студентов выбранной группы
            for student in students:
                JournalEntry.objects.create(discipline=discipline, date=date, student=student)
            # После создания журнала перенаправляем на страницу предварительного просмотра
            return redirect(reverse('preview_journal', kwargs={'discipline': discipline, 'group_id': group_id}))
    else:
        form = JournalCreationForm()
    
    return render(request, 'create_journal.html', {'form': form, 'groups': groups})

def preview_journal(request, discipline=None, group_id=None):
    if discipline is not None and group_id is not None:
        journal_entries = JournalEntry.objects.filter(discipline=discipline, student__group_id=group_id)
        
        if journal_entries.exists():
            # Generate the Excel file
            wb = generate_excel_journal(journal_entries)
            # Set the response content type to Excel
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            # Set the Content-Disposition header to make the browser treat the response as an attachment
            response['Content-Disposition'] = f'attachment; filename={force_str(discipline)}.xlsx'
            # Save the workbook to the response
            wb.save(response)
            # Return the response
            return response
        else:
            return render(request, 'preview_journal.html', {'empty_message': 'Нет данных для отображения.'})
    else:
        return render(request, 'preview_journal.html', {'error_message': 'Отсутствуют обязательные параметры в URL.'})