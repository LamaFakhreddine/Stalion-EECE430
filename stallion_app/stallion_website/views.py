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
from .forms import *
from .decorators import unauthenticated_user, allowed_users



def home(request):
    now = datetime.now()
    print("NOW", now)
    events = Event.objects.filter(datetime__gt = now).order_by('datetime')
    next_event = None
    # if no events exist, pass null
    if len(events) != 0:
        next_event = events[0]
    # print("DATTIME", next_event.datetime)
    context = {
        "next_event": next_event
    }
    return render(request, 'stallion_website/index.html', context=context)


def events(request):
    # get all events whose date has not passed yet 
    today = datetime.today()
    events = Event.objects.filter(datetime__gt = today).order_by('datetime')
    next_event = None
    # if no events exist, pass null
    if len(events) != 0:
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

def programs(request):
    programs_list = Program.objects.all()
    print(programs_list)
    return render(request, 'stallion_website/programs.html', 
    {'programs_list' : programs_list})

def programinfo(request):
    return render(request, 'stallion_website/programinfo.html')

def reserve(request):
    courts_list = Court.objects.all()
    print(courts_list)
    return render(request, 'stallion_website/reserve.html', 
    {'courts_list' : courts_list})

def reserveinfo(request):
    return render(request, 'stallion_website/reserveinfo.html')

@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if  request.user.groups.all():
                if request.user.groups.all()[0].name == 'member':
                    return redirect('memberAccount')
                elif request.user.groups.all()[0].name == 'coach':
                    return redirect('coachAccount')
                elif request.user.groups.all()[0].name == 'admin':
                    return redirect('adminAccount')
                else:
                    return redirect('home')
            else:
                messages.info(request, "This user has not been assigned a role, please try using another user")
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
            Member.objects.create(
                user=user,
                name=user.username,
                email=user.email,

            )

            messages.success(request,'Account was created for ' + username)
            
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


#@login_required(login_url='home')
#@allowed_users(allowed_roles=['admin'])
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


def members(request):
    members = Member.objects.all()
    form = FilterMembersForm(request.POST)

    return render(request, 'stallion_website/members.html', {'members': members, 'form': form})


def delete_member(request, m):
    print(m)
    User.objects.get(username=m).delete()
    members = Member.objects.all()
        
    return redirect('/members', {'members': members})

#@login_required(login_url='home')
#@allowed_users(allowed_roles=['member','coach','admin'])
def buytickets(request,pk_test): 
    print(Event.objects.get(id=pk_test)) 
    event = Event.objects.get(id=pk_test)
    context = {
        "event": event
    }
    
    event.description = event.description

    if request.method == 'POST':

        username = request.POST.get('name')
        ticket =  request.POST.get('select')

        if ticket=="Area A":
            price=100
        elif ticket=="Area B":
            price=75
        else:
            price=50

        Ticket.objects.create(
                ticket=ticket,
                price=price
            )
        EventTicket.objects.create(
                ticket=ticket,
                member= Member.objects.get(user=request.user),
                event=Event.objects.get(id=pk_test) 
            )
        
        
    return render(request, 'stallion_website/tickets.html', context = context)



def filter_member(request):
    form = FilterMembersForm(request.POST)
    members = Member.objects.all()
    if form.data['name']:
        members = members.filter(name=form["name"].value())
    if form.data['email']:
        members = members.filter(email=form["email"].value())
    if form.data['dob']:
        members = members.filter(dob=form["dob"].value())
    if form.data['phone_number']:
        members = members.filter(phone_number=form["phone_number"].value())

    return redirect('/members', {'members': members})


def update_member(request, m):
    member = Member.objects.get(name=m)
    form = UpdateMembersForm(initial={'name': getattr(member, 'name'), 'email': getattr(member, 'email'), 'dob': getattr(member, 'dob'), 'phone_number': getattr(member, 'phone_number')})
    return render(request, 'stallion_website/updateMember.html', {'form': form, 'm': m})


def save_updates(request):
    members = Member.objects.all()
    form = UpdateMembersForm(request.POST)
    m = Member.objects.get(name=form['name'].value())
    u = User.objects.get(username=form['name'].value())
    form1 = UpdateMembersForm1(request.POST, instance=m)
    form2 = UpdateUserForm(request.POST, instance=u)

    if form1.is_valid():                                                 
        form1.save()       
        form2.save()                                                                   

    return redirect('/members', {'members': members})





