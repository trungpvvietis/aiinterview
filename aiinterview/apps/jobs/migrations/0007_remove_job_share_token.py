# Generated by Django 5.2 on 2025-04-23 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_alter_job_share_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='share_token',
        ),
    ]
