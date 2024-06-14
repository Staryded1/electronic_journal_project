from django import views
from django.urls import path
from .views import (
    home, login, dashboard, logout_view, settings, 
    department_selection, admin_panel, add_group, add_specialty, 
    add_student, add_teacher, group_selection, discipline_selection, 
    create_journal, add_discipline, JournalView, JournalExportView, 
    StudentGradeView, TeacherGradeView, load_students
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings, name='settings'),
    path('department/', department_selection, name='department_selection'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('add_group/', add_group, name='add_group'),
    path('add_specialty/', add_specialty, name='add_specialty'),
    path('add_student/', add_student, name='add_student'),
    path('add_teacher/', add_teacher, name='add_teacher'),
    path('group_selection/', group_selection, name='group_selection'),
    path('discipline-selection/<int:group_id>/', discipline_selection, name='discipline_selection'),
    path('create-journal/', create_journal, name='create_journal'),
    path('add_discipline/', add_discipline, name='add_discipline'),
    path('journal/', JournalView.as_view(), name='journal_view'),
    path('journal/export/', JournalExportView.as_view(), name='journal_export'),
    path('grades/', StudentGradeView.as_view(), name='grades'),
    path('teacher_grades/', TeacherGradeView.as_view(), name='teacher_grades'),
    path('load-students/', load_students, name='load_students'),
]