from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
import json
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

    return render(request, 'event_detail.html', {'event' : event})


def accept_event(request):
    if request.method == "POST": 
        accept_list = request.user.getAcceptedEvents()

        print(accept_list)
        if len(accept_list) != 0:
            item_exists = next((item for item in accept_list if item != "" and int(item) == request.POST.get('event_id')),False)
            if not item_exists:
                request.user.addEvent(request.POST.get('event_id'))
                request.session.modified = True
        

    if request.is_ajax():
        data = {
            'event_id': request.POST.get('event_id')
        }
        request.session.modified = True
        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))


        
def deny_event(request):
    if request.method == "POST":
        request.user.removeEvent(request.POST.get('event_id'))
        request.session.modified = True 
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
            i = int(elem)
            data = {
                'event_id': i
            }
            jsn.append(data)
        

    return JsonResponse(jsn,safe=False)
    # return HttpResponse(request, data, content_type='applocation/json')
# def event_accept(request):
#     if 'elem_id' in request.POST:
#         elem_id = request.POST['elem_id']
    
