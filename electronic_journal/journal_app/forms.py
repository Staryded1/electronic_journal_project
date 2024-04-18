from django import forms
from .models import Specialty
from .models import Group
from .models import Student


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