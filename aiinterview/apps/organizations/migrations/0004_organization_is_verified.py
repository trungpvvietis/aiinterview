# Generated by Django 5.2 on 2025-04-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_alter_organization_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
