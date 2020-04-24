from django.db import models
from django.utils import timezone

class Event(models.Model):
    event_title = models.CharField('Название ивента', max_length = 100)
    event_text = models.TextField('Описание ивента')
    publish_date = models.DateTimeField('Дата публикации')
    event_status = models.CharField('Текущее состояние ивента', max_length = 50)
    event_photo = models.ImageField('Изображение для ивента', upload_to='images/', blank=True, null=True)    
