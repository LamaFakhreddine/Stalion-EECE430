# Generated by Django 4.0.4 on 2022-04-27 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stallion_website', '0003_court_memberprograms_courtreservations'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
