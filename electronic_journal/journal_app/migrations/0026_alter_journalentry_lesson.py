# Generated by Django 4.2.11 on 2024-06-07 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0025_lesson_journalentry_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='lesson',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='journal_app.lesson'),
        ),
    ]
