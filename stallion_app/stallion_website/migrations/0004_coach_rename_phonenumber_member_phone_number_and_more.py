# Generated by Django 4.0.3 on 2022-04-05 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stallion_website', '0003_alter_event_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('dob', models.DateField()),
                ('phone_number', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='member',
            old_name='phoneNumber',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='member',
            name='gender',
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stallion_website.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Dates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('M', 'Mon'), ('T', 'Tues'), ('W', 'Wed'), ('Th', 'Thurs'), ('F', 'Fri'), ('S', 'Sat'), ('Su', 'Sun')], max_length=5)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stallion_website.programs')),
            ],
        ),
    ]
