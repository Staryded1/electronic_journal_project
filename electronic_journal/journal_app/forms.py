from django import forms
from .models import Lesson, Specialty, Group, Student, Teacher, Discipline
from django.contrib.auth.models import User
from .models import JournalEntry

class SpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ['code', 'name']

class GroupForm(forms.ModelForm):
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), empty_label=None)

    class Meta:
        model = Group
        fields = ['name', 'specialty']

class StudentForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)

    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'middle_name', 'birth_year', 'group']

class TeacherForm(forms.ModelForm):
    email = forms.EmailField()
    disciplines = forms.ModelMultipleChoiceField(queryset=Discipline.objects.all(), widget=forms.SelectMultiple)

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'disciplines']

class JournalCreationForm(forms.Form):
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), label='Дисциплина')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Группа')
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='Преподаватель')
    month = forms.IntegerField(min_value=1, max_value=12, label='Месяц')
    year = forms.IntegerField(min_value=1900, max_value=2100, label='Год')

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['date', 'topic', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название дисциплины',
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.group.set(Group.objects.all())
            instance.save()
        return instance

class JournalForm(forms.Form):
    date = forms.CharField(label='Дата занятия', max_length=10)
    topic = forms.CharField(label='Название темы', max_length=100)
    description = forms.CharField(label='Описание темы', widget=forms.Textarea)