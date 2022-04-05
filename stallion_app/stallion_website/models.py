from django.db import models

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    dob = models.DateField()
    phone_number = models.IntegerField()

class Coach(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    dob = models.DateField()
    phone_number = models.IntegerField()

class Program(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.IntegerField(default=0)

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
    name = models.EmailField(max_length=200)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=300)

class Tickets(models.Model):
    TICKET_TYPE = (
        ('Area A', 'Area A'),
        ('Area B', 'Area B'),
        ('Area C', 'Area C')
    )
    ticket = models.CharField(max_length=20, choices=TICKET_TYPE)
    price = models.IntegerField()

class EventTickets(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    num_tickets = models.IntegerField()

class Admin(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)

