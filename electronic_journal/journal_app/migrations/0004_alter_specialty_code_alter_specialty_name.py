# Generated by Django 4.2.11 on 2024-04-18 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0003_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialty',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
