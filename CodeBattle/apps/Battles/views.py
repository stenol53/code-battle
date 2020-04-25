from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 , redirect

from .models import Battle

def index(request):
    return redirect("/events")

def open_battle(request,id):
    get_object_or_404(Battle, pk = id)
    return render(request,'Battles/base.html',{ 'id': id })
