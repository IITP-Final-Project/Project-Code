# Generated by Django 3.0.5 on 2020-11-20 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('day', models.CharField(max_length=10)),
                ('time', models.TimeField()),
                ('prof', models.CharField(max_length=30)),
            ],
        ),
    ]
