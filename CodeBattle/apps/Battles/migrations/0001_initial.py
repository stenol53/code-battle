# Generated by Django 3.0.5 on 2020-04-26 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0003_auto_20200426_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст ответа')),
                ('correctly', models.BooleanField(verbose_name='Верный ли вариант')),
            ],
        ),
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimeEnd', models.DateTimeField(verbose_name='Время завершения битвы')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Событие')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Вопрос')),
                ('image_url', models.FileField(upload_to=None, verbose_name='Изображение (Если нужно)')),
                ('AnswerVariant', models.ManyToManyField(to='Battles.AnswerVariant', verbose_name='Варианты ответа')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Battle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Battles.Battle')),
                ('user1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user1', to=settings.AUTH_USER_MODEL, verbose_name='Первый участник')),
                ('user2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user2', to=settings.AUTH_USER_MODEL, verbose_name='Второй участник')),
            ],
        ),
        migrations.CreateModel(
            name='Participent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isReady', models.BooleanField(verbose_name='Готовность')),
                ('Battle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Battles.Battle')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Участник')),
            ],
        ),
        migrations.AddField(
            model_name='battle',
            name='taskList',
            field=models.ManyToManyField(to='Battles.Task', verbose_name='Список заданий'),
        ),
        migrations.AddField(
            model_name='battle',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Победитель'),
        ),
    ]
