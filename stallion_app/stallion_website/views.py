from datetime import datetime
from multiprocessing import Event
from django.shortcuts import render
from django.http import HttpResponse
from .models import * 
import calendar
# Create your views here.

def home(request):
    next_event = Event.objects.filter().order_by('datetime')[0]
    today = datetime.today()
    print(today)
    context = {
        "next_event": next_event
    }
    return render(request, 'stallion_website/index.html', context=context)

def events(request):
    events = Event.objects.filter().order_by('datetime')
    next_event = events[0]
    context = {
        "events": events,
        "next_event": next_event
    }
    print(events)
    return render(request, 'stallion_website/events.html', context=context)
    
def about(request):
    return HttpResponse("ABOUT US")

def login(request):
    return render(request, 'stallion_website/login.html')