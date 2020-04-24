from django.db import models
from django.utils import timezone

class Event(models.Model):
    event_title = models.CharField('Название ивента', max_length = 100)
    event_text = models.TextField('Описание ивента')
    publish_date = models.DateTimeField('Дата публикации')
    event_status = models.CharField('Текущее состояние ивента', max_length = 50)
    event_photo = models.FileField('Изображение для ивента', upload_to='event_media', blank=True, null=True)    
    competitors_id_list = models.TextField('Список участников', blank=True)