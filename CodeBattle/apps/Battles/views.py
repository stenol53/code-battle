from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404 , redirect

from .models import Battle,Participent

def index(request):
    return redirect("/events")

def open_battle(request,id):
    get_object_or_404(Battle, pk = id)
    return render(request,'Battles/base.html',{ 'id': id })


def user_validate(request):
    if request.method == "POST":
        battle_id = request.POST.get('battle_id')
        print("battle_id",battle_id)
        battle = Battle.objects.get(pk=battle_id)

        if request.is_ajax():
            qs = Participent.objects.filter(Battle = battle).filter(User = request.user).distinct()
            print(len(qs))
            data = {
                'battle_id': battle_id,
                'user_id': request.user.id,
                'response': 0
            }
            if len(qs) is not 0:          
                data = {
                    'battle_id': battle_id,
                    'user_id': request.user.id,
                    'start_at': battle.event.publish_date,
                    'response': 1
                }
            request.session.modified = True 
            return JsonResponse(data)

    return redirect(request.POST.get('url_from'))