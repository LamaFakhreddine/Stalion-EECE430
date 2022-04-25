from datetime import datetime
from multiprocessing import Event
import re
from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import * 
import calendar
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Create your views here.
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users



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
    return render(request, 'stallion_website/About.html')


@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.all()[0].name == 'member':
                return redirect('memberAccount')
            elif request.user.groups.all()[0].name == 'coach':
                return redirect('coachAccount')
            elif request.user.groups.all()[0].name == 'admin':
                return redirect('adminAccount')
            else:
                return redirect('home')
        else:
            messages.info(request, "Username OR password is incorrect")
    context = {}
    return render(request, 'stallion_website/login.html', context)


def logoutUser(request):
    logout(request)
    return(redirect('home'))


@unauthenticated_user
def signup(request):
    
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='member')
            user.groups.add(group)
            messages.success(request,'Account was created for' + username)
            
            return redirect('login')

    context = {'form':form}
    return render(request, 'stallion_website/signup.html', context)


@login_required(login_url='home')
@allowed_users(allowed_roles=['member'])
def member(request):
    return render(request, 'stallion_website/memberAccount.html')


@login_required(login_url='home')
@allowed_users(allowed_roles=['coach'])
def coach(request):
    return render(request, 'stallion_website/coachAccount.html')


@login_required(login_url='home')
@allowed_users(allowed_roles=['admin'])
def admin(request):
    return render(request, 'stallion_website/adminAccount.html')

def profile(request):
    print("in")
    if request.user.groups.all()[0].name == 'member':
        return member(request)
    elif request.user.groups.all()[0].name == 'coach':
        return coach(request)
    elif request.user.groups.all()[0].name == 'admin':
        return admin(request)
    else:
        return redirect('home')

def contact(request):
    return render(request, 'stallion_website/contactus.html')
