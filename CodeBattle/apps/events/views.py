from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .models import Event

app_name = 'events'
def events(request):
    latest_events_list = Event.objects.order_by('-publish_date')[:5]
    if request.user.is_authenticated:
        return render(request, 'events.html', {'latest_events_list' : latest_events_list})
    else:
        return render(request,'account/login.html',{'message': "Авторизируйтесь, чтобы просматривать эту страницу"})
    

def event_details(request, event_id):
    try:
        event = Event.objects.get(id = event_id)
    except:
        raise Http404("Ивент не найден!")

    return render(request, 'event_details.html', {'event' : event})