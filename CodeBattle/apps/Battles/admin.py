from django.contrib import admin

from . import models

admin.site.register(models.Battle)
admin.site.register(models.Contact)
admin.site.register(models.Pair)
admin.site.register(models.Task)
admin.site.register(models.AnswerVariant)