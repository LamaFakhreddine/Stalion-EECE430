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
    programs_list = Program.objects.all()
    form = EnrollProgram(request.POST)
    u = request.user
    return render(request, 'stallion_website/programinfo.html', 
    {'programs_list' : programs_list, 'form': form, 'u': u})

def reserve(request):
    courts_list = Court.objects.all()
    print(courts_list)
    return render(request, 'stallion_website/reserve.html', 
    {'courts_list' : courts_list})

def reserveinfo(request):
    courts_list = Court.objects.all()
    form = CourtReservations(request.POST)
    form1 = CourtReservations(request.POST)
    return render(request, 'stallion_website/reserveinfo.html', 
    {'courts_list' : courts_list, 'form': form, 'form1': form1})


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
    memberProgs = (MemberPrograms.objects.filter(member=Member.objects.get(user=request.user))).all()
    memberEventsTick = (EventTicket.objects.filter(member=Member.objects.get(user=request.user))).all()
    memberReservations = (CourtReservations.objects.filter(member=Member.objects.get(user=request.user))).all()
    return render(request, 'stallion_website/memberAccount.html', {'memberProgs': memberProgs, 'memberEventsTick':memberEventsTick, 'memberReservations':memberReservations})


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
    User.objects.get(username=m).delete()
    members = Member.objects.all()
        
    return redirect('/members', {'members': members})

def buytickets(request,pk_test):  
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
                ticket=Ticket.objects.last(),
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

    form = FilterMembersForm()
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


def enroll(request):
    form = EnrollProgram(request.POST)
    form1 = EnrollProgram1(request.POST)
    if request.method == 'POST':
        m = Member.objects.get(name=form1['name'].value())
        p = Program.objects.get(id=form['program'].value())
        MemberPrograms.objects.create(
            member = m,
            program = p
        )

        return render(request, 'stallion_website/index.html')

def reservation(request):
    form = ReserveField(request.POST)
    form1 = ReserveField1(request.POST)
    print(form1['name'].value())
    if request.method == 'POST':
        print("im here")
        m = Member.objects.get(name=form1['name'].value())
        c = Court.objects.get(id=form['court'].value())
        rd = Court.objects.get(id=form['reservation_date'].value())
        s = Court.objects.get(id=form['start_time'].value())
        e = Court.objects.get(id=form['end_time'].value())
        CourtReservations.objects.create(
            member = m,
            court = c,
            reservation_date=rd,
            start_time=s,
            end_time=e
        )

        return render(request, 'stallion_website/index.html')





def coaches(request):
    coaches = Coach.objects.all()
    form = FilterCoachesForm(request.POST)

    return render(request, 'stallion_website/coaches.html', {'coaches': coaches, 'form': form})


def delete_coaches(request, m):
    User.objects.get(username=m).delete()
    coaches = Coach.objects.all()
        
    return redirect('/coaches', {'coaches': coaches})


def filter_coaches(request):
    form = FilterCoachesForm(request.POST)
    coaches = Coach.objects.all()
    if form.data['name']:
        coaches = coaches.filter(name=form["name"].value())
    if form.data['email']:
        coaches = coaches.filter(email=form["email"].value())
    if form.data['dob']:
        coaches = coaches.filter(dob=form["dob"].value())
    if form.data['phone_number']:
        coaches = coaches.filter(phone_number=form["phone_number"].value())
    if form.data['specialty']:
        coaches = coaches.filter(phone_number=form["specialty"].value())

    form = FilterCoachesForm()

    return redirect('/coaches', {'coaches': coaches})


def update_coaches(request, m):
    coaches = Coach.objects.get(name=m)
    form = UpdateCoachesForm(initial={'name': getattr(coaches, 'name'), 'email': getattr(coaches, 'email'), 'dob': getattr(coaches, 'dob'), 'phone_number': getattr(coaches, 'phone_number'), 'specialty': getattr(coaches, 'specialty')})
    return render(request, 'stallion_website/updateCoaches.html', {'form': form, 'm': m})


def save_updates2(request):
    coaches = Coach.objects.all()
    form = UpdateCoachesForm(request.POST)
    c = Coach.objects.get(name=form['name'].value())
    u = User.objects.get(username=form['name'].value())
    form1 = UpdateCoachesForm1(request.POST, instance=c)
    form2 = UpdateUserForm(request.POST, instance=u)

    if form1.is_valid():                                                 
        form1.save()       
        form2.save()                                                                   

    return redirect('/coaches', {'coaches': coaches})

def add_coaches(request):
    form = AddCoachesForm(request.POST)
    form1 = FilterCoachesForm(request.POST)
    if request.method == "GET":
        return render(request, 'stallion_website/addCoaches.html', {'form': form})
    else:
        if form.is_valid():
            u = User.objects.create(username=form['name'].value(), email=form['email'].value(), password=form['password'].value())
            Coach.objects.create(user=u, name=form['name'].value(), email=form['email'].value(), dob=form['dob'].value(), phone_number=form['phone_number'].value(), password=form['password'].value(), specialty=form['specialty'].value())
            coaches = Coach.objects.all()
            return redirect('/coaches', {'coaches': coaches, 'form': form})


def programs_admin(request):
    programs = Program.objects.all()
    form = FilterProgramsForm(request.POST)

    return render(request, 'stallion_website/programs-admin.html', {'programs': programs, 'form': form})


def delete_programs(request, m):
    Program.objects.get(name=m).delete()
    programs = Program.objects.all()
        
    return redirect('/programs_admin', {'programs': programs})


def filter_programs(request):
    form = FilterProgramsForm(request.POST)
    programs = Program.objects.all()

    if form.data['name']:
        programs = programs.filter(name=form["name"].value())
    if form.data['coach']:
        c = Coach.objects.get(name=form["coach"].value())
        programs = programs.filter(coach=c)
    if form.data['start_time']:
        programs = programs.filter(start_time=form["start_time"].value())
    if form.data['end_time']:
        programs = programs.filter(end_time=form["end_time"].value())
    if form.data['price']:
        programs = programs.filter(price=form["price"].value())

    form = FilterProgramsForm()

    return render(request, 'stallion_website/programs-admin.html', {'programs': programs, 'form': form})


def update_programs(request, m):
    programs = Program.objects.get(name=m)
    form = UpdateProgramsForm(initial={'name': getattr(programs, 'name'), 'coach': getattr(programs, 'coach'), 'start_time': getattr(programs, 'start_time'), 'end_time': getattr(programs, 'end_time'), 'price': getattr(programs, 'price'), 'image_url': getattr(programs, 'image_url')})
    return render(request, 'stallion_website/updatePrograms.html', {'form': form, 'm': m})


def save_updates3(request):
    programs = Program.objects.all()
    form = UpdateProgramsForm(request.POST)
    p = Program.objects.get(name=form['name'].value())
    form1 = UpdateProgramsForm(request.POST, instance=p)

    if form1.is_valid():                                                 
        form1.save()                                                                

    return redirect('/programs_admin', {'programs': programs})

def add_programs(request):
    form = UpdateProgramsForm(request.POST)
    if request.method == "GET":
        return render(request, 'stallion_website/addPrograms.html', {'form': form})
    else:
        if form.is_valid():
            c = Coach.objects.get(id=form['coach'].value())
            Program.objects.create(name=form['name'].value(), coach=c, start_time=form['start_time'].value(), end_time=form['end_time'].value(), price=form['price'].value(), image_url=form['image_url'].value())
            programs = Program.objects.all()
            return redirect('/programs_admin', {'programs': programs, 'form': form})


def courts(request):
    courts = Court.objects.all()
    form = FilterCourtsForm(request.POST)

    return render(request, 'stallion_website/courts.html', {'courts': courts, 'form': form})


def delete_courts(request, m):
    Court.objects.get(name=m).delete()
    courts = Court.objects.all()
        
    return redirect('/courts', {'courts': courts})


def filter_courts(request):
    form = FilterCourtsForm(request.POST)
    courts = Court.objects.all()

    if form.data['name']:
        courts = courts.filter(name=form["name"].value())

    form = FilterCourtsForm()
    return render(request, 'stallion_website/courts.html', {'courts': courts, 'form': form})


def update_courts(request, m):
    courts = Court.objects.get(name=m)
    form = UpdateProgramsForm(initial={'name': getattr(courts, 'name'),'image_url': getattr(courts, 'image_url')})
    return render(request, 'stallion_website/updateCourts.html', {'form': form, 'm': m})


def save_updates4(request):  
    courts = Court.objects.all()
    form = UpdateCourtsForm(request.POST)
    p = Court.objects.get(name=form['name'].value())
    form1 = UpdateCourtsForm(request.POST, instance=p)

    if form1.is_valid():                                                 
        form1.save()                                                         

    return redirect('/courts', {'courts': courts})

def add_courts(request):
    form = UpdateCourtsForm(request.POST)
    if request.method == "GET":
        return render(request, 'stallion_website/addCourts.html', {'form': form})
    else:
        if form.is_valid():
            Court.objects.create(name=form['name'].value(), image_url=form['image_url'].value())
            courts = Court.objects.all()
            return redirect('/courts', {'courts': courts, 'form': form})


def events_admin(request):
    events = Event.objects.all()
    form = FilterEventsForm(request.POST)

    return render(request, 'stallion_website/events-admin.html', {'events': events, 'form': form})


def delete_events(request, m):
    Event.objects.get(name=m).delete()
    events = Event.objects.all()
        
    return redirect('/events_admin', {'events': events})


def filter_events(request):
    form = FilterEventsForm(request.POST)
    events = Event.objects.all()

    if form.data['name']:
        events = events.filter(name=form["name"].value())
    if form.data['datetime']:
        events = events.filter(datetime=form["datetime"].value())
    if form.data['location']:
        events = events.filter(location=form["location"].value())

    form = FilterEventsForm()
    return render(request, 'stallion_website/events-admin.html', {'events': events, 'form': form})


def update_events(request, m):
    events = Event.objects.get(name=m)
    form = UpdateEventsForm(initial={'name': getattr(events, 'name'),'datetime': getattr(events, 'datetime'), 'location': getattr(events, 'location'), 'description': getattr(events, 'description')})
    return render(request, 'stallion_website/updateEvents.html', {'form': form, 'm': m})


def save_updates5(request):  
    events = Event.objects.all()
    form = UpdateEventsForm(request.POST)
    p = Event.objects.get(name=form['name'].value())
    form1 = UpdateEventsForm(request.POST, instance=p)

    if form1.is_valid():                                                 
        form1.save()  

    form = UpdateEventsForm()                                                       
    return render(request, 'stallion_website/events-admin.html', {'events': events, 'form': form})

def add_events(request):
    form = UpdateEventsForm(request.POST)
    if request.method == "GET":
        return render(request, 'stallion_website/addEvents.html', {'form': form})
    else:
        if form.is_valid():
            Event.objects.create(name=form['name'].value(), datetime=form['datetime'].value(), location=form['location'].value(), description=form['description'].value())
            events = Event.objects.all()
            return redirect('/events_admin', {'events': events, 'form': form})





        






