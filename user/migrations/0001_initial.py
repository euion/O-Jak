# Generated by Django 2.2.4 on 2021-01-25 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('student_ID', models.CharField(max_length=45, unique=True)),
                ('User_PW', models.CharField(max_length=256)),
                ('smoke', models.IntegerField()),
                ('gender', models.CharField(max_length=5)),
                ('tendency', models.CharField(max_length=15)),
                ('lifetime', models.CharField(max_length=20)),
                ('major', models.CharField(max_length=45)),
                ('age', models.IntegerField()),
                ('religion', models.CharField(max_length=45)),
                ('labtop', models.IntegerField()),
                ('police', models.IntegerField()),
                ('admin', models.IntegerField()),
                ('sleepinghabit', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
