# Generated by Django 4.2.11 on 2024-05-22 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0020_alter_journalentry_day_alter_journalentry_month_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='teacher',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='journal_app.teacher'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='disciplines',
            field=models.ManyToManyField(related_name='teachers', to='journal_app.discipline'),
        ),
    ]
