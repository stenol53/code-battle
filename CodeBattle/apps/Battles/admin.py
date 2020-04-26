from django.contrib import admin

from .models import Battle, Participent, Task, AnswerVariant, Round


# from .models import Thread, ChatMessage

# class ChatMessage(admin.TabularInline):
#     model = ChatMessage

# class ThreadAdmin(admin.ModelAdmin):
#     inlines = [ChatMessage]
#     class Meta:
#         model = Thread 


# admin.site.register(Thread, ThreadAdmin)


class Participent(admin.TabularInline):
    model = Participent

class Round(admin.TabularInline):
    model = Round

class Task(admin.TabularInline):
    model = Task

# class AnswerVariant(admin.TabularInline):
#     model = AnswerVariant

class BattleAdmin(admin.ModelAdmin):
    inlines = [Participent, Round, Task]
    class Meta:
        model = Battle

# class TaskAdmin(admin.TabularInline):
#     inlines = [AnswerVariant]
#     class Meta:
#         model = Task

admin.site.register(Battle,BattleAdmin)
# admin.site.register(Task,TaskAdmin)


# admin.site.register(models.Battle)
# admin.site.register(Task)
admin.site.register(AnswerVariant)
# admin.site.register(models.Participent)