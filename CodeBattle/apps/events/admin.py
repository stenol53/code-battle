from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'event_text', 'publish_date', 'event_status', 'event_photo')
    

admin.site.register(Event, EventAdmin)