from django import forms
from .models import Specialty, Group, Student, Teacher, Discipline
from django.contrib.auth.models import User

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
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=True, label="Дисциплина")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Группа")
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), required=True, label="Преподаватель")

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
