from django.db import models

class Specialty(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)  # Поле для связи с моделью Specialty

    def __str__(self):
        return self.name
    
class Student(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birth_year = models.IntegerField()
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}"