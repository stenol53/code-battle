# Generated by Django 3.0.5 on 2020-04-24 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_event_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='publish_time',
            new_name='publish_date',
        ),
    ]