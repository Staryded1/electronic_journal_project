# Generated by Django 4.2.11 on 2024-05-16 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0013_alter_teacher_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='password',
        ),
    ]