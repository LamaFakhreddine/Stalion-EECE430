# Generated by Django 4.0.3 on 2022-04-05 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
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
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField()),
                ('location', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=300)),
            ],
            options={
                'unique_together': {('datetime', 'location')},
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('dob', models.DateField()),
                ('phone_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(choices=[('Area A', 'Area A'), ('Area B', 'Area B'), ('Area C', 'Area C')], max_length=20)),
                ('price', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stallion_website.event')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('price', models.IntegerField(default=0)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stallion_website.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('M', 'Mon'), ('T', 'Tues'), ('W', 'Wed'), ('Th', 'Thurs'), ('F', 'Fri'), ('S', 'Sat'), ('Su', 'Sun')], max_length=5)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stallion_website.program')),
            ],
        ),
    ]