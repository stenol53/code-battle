# Generated by Django 3.0.5 on 2020-04-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Battles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='friends',
        ),
        migrations.AlterField(
            model_name='battle',
            name='TimeEnd',
            field=models.DateTimeField(verbose_name='Время начала битвы'),
        ),
        migrations.AlterField(
            model_name='battle',
            name='TimeStart',
            field=models.DateTimeField(verbose_name='Время завершения битвы'),
        ),
    ]
