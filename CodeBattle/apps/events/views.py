from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
import json
from .models import Event
from Battles.models import Battle, Participent 

app_name = 'events'
def events(request):
    latest_events_list = Event.objects.order_by('-publish_date')[:5]
    if request.user.is_authenticated:
        return render(request, 'events.html', {'latest_events_list' : latest_events_list})
    else:
        return render(request,'account/login.html',{'message': "Авторизируйтесь, чтобы просматривать эту страницу"})
    

def event_details(request):
    if request.method == "GET":
        event_id = request.GET.get('event_id')
        event = Event.objects.get(id = event_id)
        print(event)
        print(event.get_users_count())
        data = {
            'title' : event.event_title,
            'text' : event.event_text,
            'date' : event.publish_date,
            'status' : event.event_status,
            'users_count' : event.get_users_count(),

        }
        if event.event_photo:
            data['photo'] = event.event_photo.url

        return JsonResponse(data)
    # try:
    #     event = Event.objects.get(id = event_id)
    # except:
    #     raise Http404("Ивент не найден!")

    # return render(request, 'event_details.html', {'event' : event})



def accept_event(request):
    if request.method == "POST": 
        accept_list = request.user.getAcceptedEvents()

        print(accept_list)
        if len(accept_list) != 0:
            item_exists = next((item for item in accept_list if item != "" and item == request.POST.get('event_id')),False)
            if not item_exists:
                request.user.addEvent(request.POST.get('event_id'))
                request.session.modified = True
                id = request.POST.get('event_id')
                ev = Event.objects.get(id = id)
                battle = Battle.objects.get(pk=id)
                Participent.objects.create(Battle=battle, User=request.user, isReady = False)
                ev.add_user_to_list(request.user.id)


                print(ev.get_users())
        

    if request.is_ajax():
        data = {
            'event_id': request.POST.get('event_id')
        }
        request.session.modified = True 
        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))
        
def deny_event(request):
    if request.method == "POST":
        id = request.POST.get('event_id')
        request.user.removeEvent(id)
        request.session.modified = True 
        ev = Event.objects.get(id=id)
        ev.remove_user_from_list(request.user.id)
        print(ev.get_users())
        for elem in Battle.objects.all():
            print(elem.id)
        battle = Battle.objects.get(pk=id)
        Participent.objects.filter(Battle=battle).filter(User=request.user).delete()

    if request.is_ajax():
        data = {
            'event_id': request.POST.get('event_id')
        }
        request.session.modified = True
        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))

def get_events_api(request):
    # return JsonResponse(request.session.get('event_list'),safe = False)
    lst = request.user.getAcceptedEvents()
    jsn = list()
    for elem in lst:
        if elem:
            i = elem
            data = {
                'event_id': i
            }
            jsn.append(data)
        

    return JsonResponse(jsn,safe=False)
    # return HttpResponse(request, data, content_type='applocation/json')
# def event_accept(request):
#     if 'elem_id' in request.POST:
#         elem_id = request.POST['elem_id']
    