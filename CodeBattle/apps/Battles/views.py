from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 , redirect

from .models import Battle

def index(request):
    return redirect("events/events.html")

# def open_battle(request,id):
#     if get_object_or_404(Battle.objects.get(id = id))
