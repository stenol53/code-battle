from django.db import models
# from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class BattleManager(models.Manager):
    def by_id(self, id):
        qlookup = Q(id=id)
        qs = self.get_queryset().filter(qlookup).distinct()
        return qs

    def get_data(self, id):
        qlookup = Q(id = id)
        qs = self.get_queryset().filter(qlookup).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else: return None, False

class AnswerVariant(models.Model):
    text = models.TextField(("Текст ответа"))
    correctly = models.BooleanField("Верный ли вариант")

class Task(models.Model):
    question = models.TextField(("Вопрос"))
    image_url = models.FileField(("Изображение (Если нужно)"), upload_to=None, max_length=100)
    AnswerVariant = models.ManyToManyField(AnswerVariant, verbose_name=("Варианты ответа"))

class Pair(models.Model):
    user1 = models.ForeignKey(User, verbose_name=("Первый участник"),related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, verbose_name=("Второй участник"),related_name='user2', on_delete=models.CASCADE)

    def __str__(self):
        return self.user1.username + " VS " + self.user2.username

class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name=("Друзья"),related_name=("friends"), on_delete=models.CASCADE)
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.user.username

class Battle(models.Model):
    event = models.ForeignKey("events.Event", verbose_name=("Событие"), on_delete=models.CASCADE)
    participants = models.ManyToManyField(Contact, verbose_name=("Участники"))
    currentPair = models.ForeignKey(Pair, verbose_name=("Текщая пара"), on_delete=models.CASCADE)
    taskList = models.ManyToManyField(Task, verbose_name=("Список заданий"))
    winner = models.ForeignKey(User, verbose_name=("Победитель"), on_delete=models.CASCADE)
    TimeEnd = models.DateTimeField(("Время начала битвы"), auto_now=False, auto_now_add=False)
    TimeStart = models.DateTimeField(("Время завершения битвы"), auto_now=False, auto_now_add=False)
    timestamp    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.event.event_title
        return "123"
    # def is_active(self):
    #     if timezone.now > self.TimeEnd :
    #         return False
    #     return True





# class Thread(models.Model):


#     first        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
#     second       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
#     updated      = models.DateTimeField(auto_now=True)
#     timestamp    = models.DateTimeField(auto_now_add=True)
    
#     objects      = ThreadManager()

#     # @property
#     # def room_group_name(self):
#     #     return f'chat_{self.id}'

#     # def broadcast(self, msg=None):
#     #     if msg is not None:
#     #         broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
#     #         return True
#     #     return False


# class ChatMessage(models.Model):
#     thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
#     user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
#     message     = models.TextField()
#     timestamp   = models.DateTimeField(auto_now_add=True)





# class Battle