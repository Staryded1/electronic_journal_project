from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home, name='home'),  # Страница home
    path('registration/', views.registration, name='registration'),  # Страница регистрации
    path('login/', views.login, name='login'),  # Страница входа
    path('dashboard/', views.dashboard, name='dashboard'),  # Страница dashboard
    path('logout/', views.logout_view, name='logout'),
    path('grades/', views.grades, name='grades'),
    path('settings/', views.settings, name='settings'),
    path('mark/', views.mark, name='mark'),
    path('department/', views.department_selection, name='department_selection'),
    path('admin_panel/', views.admin_panel, name='admin_panel'), 
    path('add_group/', views.add_group, name='add_group'),
    path('add_specialty/', views.add_specialty, name='add_specialty'),  # Маршрут для добавления специальности
    path('add_student/', views.add_student, name='add_student'),  # URL-маршрут для добавления студента
   
]