from django.db import models
from django.contrib.auth.models import User

class Specialty(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birth_year = models.IntegerField()
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}"
    
class Discipline(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=True)
    disciplines = models.ManyToManyField('Discipline', related_name='teachers')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class JournalEntry(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    mark = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.student} - {self.discipline}'
