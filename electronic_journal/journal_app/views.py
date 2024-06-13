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
from .forms import DisciplineForm, SpecialtyForm  # Импорт вашей формы для специальностей
from .models import Specialty, Teacher  # Импорт вашей модели для специальностей
from django.contrib.admin.views.decorators import staff_member_required
from .forms import GroupForm, StudentForm
import random
import string
import pandas as pd
from .models import Student,  Lesson
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
from django.contrib.auth.decorators import user_passes_test
from .models import Specialty, Group, Discipline
from datetime import datetime
import calendar
from calendar import monthrange
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import JournalForm
from django.views.generic import FormView, ListView



def home(request):
    return render(request, 'home.html')


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

@login_required
def group_selection(request):
    is_teacher = request.user.groups.filter(name='teacher').exists()
    is_admin = request.user.groups.filter(name='admin').exists()
    
    if request.method == 'POST':
        selected_group_id = request.POST.get('group')
        if selected_group_id:
            return redirect('discipline_selection', group_id=selected_group_id)

    groups = Group.objects.all()
    return render(request, 'group_selection.html', {'is_teacher': is_teacher, 'is_admin': is_admin, 'groups': groups})

@login_required
def discipline_selection(request, group_id):
    is_teacher = request.user.groups.filter(name='teacher').exists()
    is_admin = request.user.groups.filter(name='admin').exists()

    group = get_object_or_404(Group, id=group_id)
    
    teacher = None
    if is_teacher:
        teacher = get_object_or_404(Teacher, user=request.user)

    if teacher:
        disciplines = Discipline.objects.filter(teachers=teacher, group=group)
    else:
        disciplines = Discipline.objects.filter(group=group)

    if request.method == 'POST':
        selected_discipline_id = request.POST.get('discipline')
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')

        if selected_discipline_id and selected_month and selected_year:
            return redirect(f'/journal/?discipline_id={selected_discipline_id}&group_id={group_id}&month={selected_month}&year={selected_year}')

    current_year = datetime.now().year
    years = list(range(current_year - 5, current_year + 1))
    months = [
        (1, "Январь"), (2, "Февраль"), (3, "Март"), (4, "Апрель"), (5, "Май"), (6, "Июнь"),
        (7, "Июль"), (8, "Август"), (9, "Сентябрь"), (10, "Октябрь"), (11, "Ноябрь"), (12, "Декабрь")
    ]
    return render(request, 'discipline_selection.html', {
        'is_teacher': is_teacher,
        'is_admin': is_admin,
        'disciplines': disciplines,
        'years': years,
        'months': months,
        'group': group,
    })

class JournalView(LoginRequiredMixin, FormView):
    template_name = 'journal_view.html'
    form_class = JournalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discipline_id = self.request.GET.get('discipline_id')
        group_id = self.request.GET.get('group_id')
        year = int(self.request.GET.get('year'))
        month = int(self.request.GET.get('month'))

        context['discipline'] = get_object_or_404(Discipline, id=discipline_id)
        context['group'] = get_object_or_404(Group, id=group_id)
        context['year'] = year
        context['month'] = month
        context['days'] = [day for day in range(1, 32)]
        context['students'] = Student.objects.filter(group=context['group'])
        context['journal_entries'] = JournalEntry.objects.filter(
            discipline=context['discipline'], 
            student__in=context['students'], 
            year=year, 
            month=month
        ).select_related('student', 'lesson')
        context['is_teacher'] = self.request.user.groups.filter(name='teacher').exists()
        context['is_admin'] = self.request.user.is_superuser

        context['existing_months'] = JournalEntry.objects.filter(
            discipline=context['discipline'],
            student__in=context['students'],
            year=year
        ).values_list('month', flat=True).distinct()

        return context

    def post(self, request, *args, **kwargs):
        discipline_id = self.request.GET.get('discipline_id')
        group_id = self.request.GET.get('group_id')
        year = int(self.request.GET.get('year'))
        month = int(self.request.GET.get('month'))

        discipline = get_object_or_404(Discipline, id=discipline_id)
        group = get_object_or_404(Group, id=group_id)
        students = Student.objects.filter(group=group)
        days = [day for day in range(1, 32)]
        teacher = get_object_or_404(Teacher, user=request.user)

        errors = []
        success_count = 0

        for student in students:
            for day in days:
                mark_key = f'mark_{student.id}_{day}'
                mark = request.POST.get(mark_key)
                if mark:
                    try:
                        entry, created = JournalEntry.objects.get_or_create(
                            student=student,
                            discipline=discipline,
                            day=day,
                            month=month,
                            year=year,
                            defaults={'mark': mark, 'teacher': teacher}
                        )
                        if not created:
                            entry.mark = mark
                            entry.save()
                        success_count += 1
                    except Exception as e:
                        errors.append(f"Ошибка при сохранении оценки для студента {student.id} на день {day}: {e}")

        if errors:
            messages.error(request, 'Произошли ошибки при сохранении оценок: ' + ', '.join(errors))
        else:
            messages.success(request, f'Оценки успешно сохранены.')

        return redirect(f'/journal/?discipline_id={discipline.id}&group_id={group.id}&year={year}&month={month}')

class JournalExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        discipline_id = request.GET.get('discipline_id')
        group_id = request.GET.get('group_id')
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))

        discipline = get_object_or_404(Discipline, id=discipline_id)
        group = get_object_or_404(Group, id=group_id)
        students = Student.objects.filter(group=group)
        journal_entries = JournalEntry.objects.filter(
            discipline=discipline, 
            student__in=students, 
            year=year, 
            month=month
        )

        # Получение количества дней в месяце
        _, num_days = calendar.monthrange(year, month)

        data = []
        for student in students:
            student_data = [f"{student.last_name} {student.first_name} {student.middle_name}"]
            for day in range(1, num_days + 1):
                entry = journal_entries.filter(student=student, day=day).first()
                student_data.append(entry.mark if entry else '')
            data.append(student_data)

        df = pd.DataFrame(data, columns=['Студент'] + [str(day) for day in range(1, num_days + 1)])
        
        # Запись данных в Excel с настройкой ширины столбца
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="journal_{year}_{month}.xlsx"'
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Journal')
            worksheet = writer.sheets['Journal']
            worksheet.column_dimensions['A'].width = 30  # Задаем ширину столбца 'A' (столбец с ФИО)

        return response
    
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


@staff_member_required
def add_discipline(request):
    if request.method == 'POST':
        form = DisciplineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дисциплина успешно добавлена.')
            return redirect('add_discipline')
    else:
        form = DisciplineForm()
    
    return render(request, 'add_discipline.html', {'form': form})

@staff_member_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = generate_password()  # Генерируем пароль
            teacher_role_group, created = AuthGroup.objects.get_or_create(name='teacher')  # Получаем или создаем группу ролей "teacher"
            try:
                # Создаем преподавателя
                teacher = form.save(commit=False)
                if not User.objects.filter(username=email).exists():
                    # Создаем пользователя
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name']
                    )
                    teacher.user = user
                    teacher.password = password  # Сохраняем пароль в модели Teacher без хеширования
                    teacher.save()
                    form.save_m2m()  # Сохраняем связи many-to-many для дисциплин

                    # Добавляем пользователя в группу "teacher"
                    user.groups.add(teacher_role_group)
                    
                    messages.success(request, f'Преподаватель успешно добавлен. Логин: {email}, Пароль: {password}')
                else:
                    messages.error(request, f'Пользователь с email {email} уже существует.')
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

@staff_member_required
def create_journal(request):
    groups = Group.objects.all()

    if request.method == 'POST':
        form = JournalCreationForm(request.POST)
        if form.is_valid():
            discipline = form.cleaned_data['discipline']
            group = form.cleaned_data['group']
            teacher = form.cleaned_data['teacher']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            students = group.student_set.all()

            # Удаляем существующие записи для предотвращения дублирования
            JournalEntry.objects.filter(discipline=discipline, student__in=students, month=month, year=year).delete()

            # Создание урока по умолчанию, если его еще нет
            lesson, created = Lesson.objects.get_or_create(
                date='2023-01-01',
                topic='Default Lesson',
                description='This is a default lesson.',
                discipline=discipline,
                teacher=teacher
            )

            # Создаем новые записи с значениями по умолчанию
            for student in students:
                JournalEntry.objects.create(
                    discipline=discipline,
                    student=student,
                    teacher=teacher,
                    mark=0,
                    lesson=lesson,
                    month=month,
                    year=year
                )

            # Перенаправляем на страницу административной панели
            return redirect(reverse('admin_panel'))  # Или другая страница, куда нужно перенаправить
        else:
            return render(request, 'create_journal.html', {'form': form, 'groups': groups, 'error_message': 'Форма невалидна.'})
    else:
        form = JournalCreationForm()

    return render(request, 'create_journal.html', {'form': form, 'groups': groups})