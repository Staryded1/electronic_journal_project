# Generated by Django 4.2.11 on 2024-04-18 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0005_group_specialty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='description',
        ),
    ]
