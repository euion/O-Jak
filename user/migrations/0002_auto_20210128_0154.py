# Generated by Django 2.2.3 on 2021-01-28 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='student_ID',
            field=models.CharField(max_length=45),
        ),
    ]
