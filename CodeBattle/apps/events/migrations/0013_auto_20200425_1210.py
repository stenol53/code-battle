# Generated by Django 3.0.5 on 2020-04-25 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20200425_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.CharField(default='Еще не начался', max_length=20, verbose_name='Текущее состояние ивента'),
        ),
    ]