from django.db import models
from django.utils import timezone

class Event(models.Model):
    event_title = models.CharField('Название ивента', max_length = 34)
    event_text = models.TextField('Описание ивента')
    publish_date = models.DateTimeField('Дата публикации')
    event_status = models.CharField('Текущее состояние ивента', max_length = 20, default="Еще не начался")
    event_photo = models.FileField('Изображение для ивента', upload_to='event_media', blank=True, null=True)    
    competitors_id_list = models.TextField('Список участников', blank=True, default="")

    def get_text_preview(self):
        if len(str(self.event_text)) >= 300:
            return str(self.event_text)[:300] + "..."
        else:
            return str(self.event_text)

    def get_users_count(self):
        return len(self.competitors_id_list.split(",")) - 1

    def get_users(self):
      return str(self.competitors_id_list).split(",")

    def remove_user_from_list(self,id):
        if self.has_user_in_list(id):
            lst = str(self.competitors_id_list).split(",")
            lst.remove(str(id))
            self.competitors_id_list = ",".join(lst)
            self.save()
            return True
        return False    
      
    def add_user_to_list(self,id):
        if not self.has_user_in_list(id):
            lst = str(self.competitors_id_list).split(",")
            lst.append(str(id))
            self.competitors_id_list = ",".join(lst)
            self.save()
            return True
        return False

    def has_user_in_list(self,id):
        lst = str(self.competitors_id_list).split(",")
        for elem in lst:
            if str(id) == elem:
                return True
        return False

    def __str__(self):
        return self.event_title
    
