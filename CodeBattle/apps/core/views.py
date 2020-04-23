from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect

def index(request):
    return render(request,'core/index.html')
