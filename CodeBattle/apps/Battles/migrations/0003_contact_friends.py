# Generated by Django 3.0.5 on 2020-04-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Battles', '0002_auto_20200425_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_contact_friends_+', to='Battles.Contact'),
        ),
    ]
