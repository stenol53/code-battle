from django.db import models
# from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

User = get_user_model()

class AnswerVariant(models.Model):
    text = models.TextField(("Текст ответа"))
    correctly = models.BooleanField("Верный ли вариант")

class Task(models.Model):
    question = models.TextField(("Вопрос"))
    image_url = models.FileField(("Изображение (Если нужно)"), upload_to=None, max_length=100)
    AnswerVariant = models.ManyToManyField(AnswerVariant, verbose_name=("Варианты ответа"))


class Battle(models.Model):
    event = models.ForeignKey("events.Event", verbose_name=("Событие"), on_delete=models.CASCADE)
    taskList = models.ManyToManyField(Task, verbose_name=("Список заданий")) 
    # TimeStart = models.DateTimeField(("Время начала битвы"), auto_now=False, auto_now_add=False)
    TimeEnd = models.DateTimeField(("Время завершения битвы"), auto_now=False, auto_now_add=False)
    winner = models.ForeignKey(User, null=True, blank=True, verbose_name=("Победитель"), on_delete=models.SET_NULL)



class Round(models.Model):
    Battle = models.ForeignKey(Battle, null=True, blank=True, on_delete=models.SET_NULL)
    user1 = models.ForeignKey(User,null=True,blank=True, verbose_name=("Первый участник"),related_name='user1', on_delete=models.SET_NULL)
    user2 = models.ForeignKey(User,null=True,blank=True,verbose_name=("Второй участник"),related_name='user2', on_delete=models.SET_NULL)



class Participent(models.Model):
    Battle = models.ForeignKey(Battle, null=True, blank=True, on_delete=models.SET_NULL)
    User  = models.ForeignKey(User,verbose_name="Участник",on_delete=models.CASCADE)
    isReady = models.BooleanField("Готовность")


@receiver(post_save, sender=Participent)
def participent_added(sender, instance, **kwargs):
    print(instance)

    user = instance.User
    qlookup = Q(user1=user) | Q(user2=user)
    qlookup2 = Q(user1=user) & Q(user2=user)
    qs = Round.objects.filter(Battle=instance.Battle).filter(qlookup).exclude(qlookup2).distinct()
    qlookup = Q(user1=None) | Q(user2=None)
    qlookup2 = Q(user1=None) & Q(user2=None)
    free_qs = Round.objects.filter(Battle=instance.Battle).filter(qlookup).exclude(qlookup2).distinct()
    print("Раунды с этим пользователем")
    print(qs)
    print("Раунды со свободным местом")
    print(free_qs)
    if len(qs) != 0:
        print(len(qs))
    else:
        if(len(free_qs) != 0):
            if free_qs[0].user1 is None:
                free_qs[0].user1 = user
                free_qs[0].save()
                print("Добавили в раунд на место пользователя 1")
            else: 
                print("Добавили в раунд на место пользователя 2")
                free_qs[0].user2 = user
                free_qs[0].save()
        else:
            Round.objects.create(Battle=instance.Battle,user1=user)
            print("Create Round")

@receiver(post_delete, sender=Participent)
def participent_deleted(sender, instance, **kwargs):
    print(instance)
    user = instance.User
    qlookup = Q(user1=user) | Q(user2=user)
    qlookup2 = Q(user1=user) & Q(user2=user)
    qs = Round.objects.filter(Battle=instance.Battle).filter(qlookup).exclude(qlookup2).distinct()
    for elem in qs:
        if elem.user1 == user:
            elem.user1 = None
            elem.save()
            print("Delete user1 from Round")
        if elem.user2 == user:
            elem.user2 = None
            elem.save()
            print("Delete user2 from Round")
        if elem.user1 == None and elem.user2 == None:
            print("Round is none. Delete round")
            elem.delete()
    print(qs)

# post_save.connect(participent_added,sender=Participent)

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