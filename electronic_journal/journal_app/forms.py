from django import forms
from .models import Specialty
from .models import Group
from .models import Student
from .models import Teacher
from .models import Discipline
from django.contrib.auth.models import User


class SpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ['code', 'name']

class GroupForm(forms.ModelForm):
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), empty_label=None)  # Добавляем поле для выбора специальности

    class Meta:
        model = Group
        fields = ['name',  'specialty']  # Убедитесь, что поле 'specialty' добавлено в список полей формы

class StudentForm(forms.ModelForm):
    group_id = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)  # Поле для выбора группы

    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'middle_name', 'birth_year', 'group_id']


class TeacherForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        teacher = super().save(commit=False)
        email = self.cleaned_data['email']
        # Создаем пользователя с использованием электронной почты в качестве имени пользователя (username)
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=User.objects.make_random_password()
        )
        teacher.user = user
        if commit:
            teacher.save()
        return teacher
    
class JournalCreationForm(forms.Form):
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all())
    date = forms.DateField()
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())