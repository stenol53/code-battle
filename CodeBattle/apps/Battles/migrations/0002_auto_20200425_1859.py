# Generated by Django 3.0.5 on 2020-04-25 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Battles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pair',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL, verbose_name='Первый участник'),
        ),
        migrations.AddField(
            model_name='pair',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to=settings.AUTH_USER_MODEL, verbose_name='Второй участник'),
        ),
        migrations.AddField(
            model_name='contact',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_contact_friends_+', to='Battles.Contact'),
        ),
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL, verbose_name='Друзья'),
        ),
        migrations.AddField(
            model_name='battle',
            name='currentPair',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Battles.Pair', verbose_name='Текщая пара'),
        ),
        migrations.AddField(
            model_name='battle',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Событие'),
        ),
        migrations.AddField(
            model_name='battle',
            name='participants',
            field=models.ManyToManyField(to='Battles.Contact', verbose_name='Участники'),
        ),
        migrations.AddField(
            model_name='battle',
            name='taskList',
            field=models.ManyToManyField(to='Battles.Task', verbose_name='Список заданий'),
        ),
        migrations.AddField(
            model_name='battle',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Победитель'),
        ),
    ]