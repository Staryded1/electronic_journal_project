# Generated by Django 4.2.11 on 2024-05-18 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0019_alter_journalentry_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
