# Generated by Django 5.2 on 2025-04-24 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_remove_job_share_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobinterviewconfig',
            name='categories',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
