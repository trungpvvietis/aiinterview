# Generated by Django 5.2 on 2025-04-23 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_job_employment_type_alter_job_experience_level_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='title',
        ),
    ]
