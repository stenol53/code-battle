# Generated by Django 3.0.5 on 2020-04-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20200425_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_text',
            field=models.TextField(verbose_name='Описание ивента'),
        ),
    ]