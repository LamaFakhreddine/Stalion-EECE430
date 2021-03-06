from tkinter import CASCADE
from turtle import ondrag
from django.db import models
import calendar
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE )
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)
    dob = models.DateField(null=True)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Coach(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE )
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    dob = models.DateField()
    phone_number = models.IntegerField()

    def __str__(self):
        return self.name

class Admin(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)

class Program(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.IntegerField(default=0)
    image_url = models.URLField(max_length=300, null=True)

    def __str__(self):
        return self.name

class MemberPrograms(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

class Date(models.Model):
    WEEK_DAYS = (
        ('M', 'Mon'),
        ('T', 'Tues'),
        ('W', 'Wed'),
        ('Th', 'Thurs'), 
        ('F', 'Fri'),
        ('S', 'Sat'),
        ('Su', 'Sun')
    )
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    day = models.CharField(max_length=5, choices=WEEK_DAYS)

class Event(models.Model):
    class Meta:
        unique_together = ('datetime', 'location')
    name = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    def __str__(self):
        return self.name
    
    @property
    def month_name(self):
        return calendar.month_name[self.datetime.month]
    
    @property
    def day_number(self):
        return self.datetime.date().day

class Ticket(models.Model):
    TICKET_TYPE = (
        ('Area A ($100)', 'Area A ($100)'),
        ('Area B ($75)', 'Area B ($75)'),
        ('Area C ($50)', 'Area C ($50)')
    )
    ticket = models.CharField(max_length=20, choices=TICKET_TYPE)
    price = models.IntegerField()
    def __str__(self):
        return self.ticket
    
class EventTicket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    def __str__(self):
        return self.member.name + "---" + self.event.name

class Court(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image_url = models.URLField(max_length=300, null=True)

class CourtReservations(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.member.name + "---" + self.court.name



