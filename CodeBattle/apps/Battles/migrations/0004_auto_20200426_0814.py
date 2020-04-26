# Generated by Django 3.0.5 on 2020-04-26 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Battles', '0003_task_t_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='taskList',
        ),
        migrations.AddField(
            model_name='answervariant',
            name='t_id',
            field=models.IntegerField(default=1, verbose_name='ID_IN_QUESTION'),
        ),
        migrations.AddField(
            model_name='task',
            name='av_count',
            field=models.IntegerField(default=0, verbose_name='ANSWER_VARIANTS_COUNT'),
        ),
    ]
