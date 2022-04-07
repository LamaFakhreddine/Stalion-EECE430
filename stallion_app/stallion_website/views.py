from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'stallion_website/index.html')

def about(request):
    return HttpResponse("ABOUT US")

def login(request):
    return render(request, 'stallion_website/login.html')