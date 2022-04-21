from datetime import datetime
from multiprocessing import Event
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import * 
import calendar
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .forms import CreateUserForm

def home(request):
    now = datetime.now()
    print("NOW", now)
    next_event = Event.objects.filter(datetime__gt = now).order_by('datetime')[0]
    print("DATTIME", next_event.datetime)
    context = {
        "next_event": next_event
    }
    return render(request, 'stallion_website/index.html', context=context)

def events(request):
    # get all events whose date has not passed yet 
    today = datetime.today()
    events = Event.objects.filter(datetime__gt = today).order_by('datetime')
    next_event = events[0]

    if request.method == 'GET':
        context = {
            "events": events,
            "next_event": next_event
        }
        print(events)
        return render(request, 'stallion_website/events.html', context=context)
    
    if request.method == 'POST':
        filter = request.POST.get("filter")
        # if there is no filter, redirect to page
        # else render the page with the new filtered events 
        if filter is None or filter == "":
            return redirect("events")    
        events = Event.objects.filter(name__contains=filter).order_by('datetime')
        context = {
            "events": events,
            "next_event": next_event
        }
        return render(request, 'stallion_website/events.html', context=context)
    else:
        render("Bad request!")  

def about(request):
    return HttpResponse("ABOUT US")

def login(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'stallion_website/login.html', context)

def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'stallion_website/signup.html', context)
	
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'stallion_website/register.html', context)
	

def member(request):
    return render(request, 'stallion_website/memberAccount.html')

def coach(request):
    return render(request, 'stallion_website/coachAccount.html')