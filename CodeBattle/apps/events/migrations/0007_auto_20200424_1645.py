# Generated by Django 3.0.5 on 2020-04-24 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20200424_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_photo',
            field=models.FileField(blank=True, null=True, upload_to='event_media', verbose_name='Изображение для ивента'),
        ),
    ]