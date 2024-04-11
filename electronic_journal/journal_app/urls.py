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
]