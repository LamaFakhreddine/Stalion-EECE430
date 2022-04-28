from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

#from .models import Order

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FilterMembersForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    dob = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)

class UpdateMembersForm(ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'dob', 'phone_number']

class UpdateMembersForm1(ModelForm):
    class Meta:
        model = Member
        fields = ['email', 'dob', 'phone_number']

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class FilterCoachesForm(forms.Form):
    name = forms.CharField(required=False)
    specialty = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    dob = forms.DateField(required=False)
    phone_number = forms.IntegerField(required=False)

class UpdateCoachesForm(ModelForm):
    class Meta:
        model = Coach
        fields = ['name', 'email', 'specialty', 'dob', 'phone_number']

class AddCoachesForm(ModelForm):
    class Meta:
        model = Coach
        fields = ['name', 'email', 'specialty', 'dob', 'phone_number', 'password']


class UpdateCoachesForm1(ModelForm):
    class Meta:
        model = Coach
        fields = ['email', 'specialty', 'dob', 'phone_number']

class FilterProgramsForm(forms.Form):
    name = forms.CharField(required=False)
    coach = forms.CharField(required=False)
    start_time = forms.TimeField(required=False)
    end_time = forms.TimeField(required=False)
    price = forms.IntegerField(required=False)


class UpdateProgramsForm(ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'coach', 'start_time', 'end_time', 'price', 'image_url']

class FilterCourtsForm(forms.Form):
    name = forms.CharField(required=False)
    image_url = forms.URLField(required=False)


class UpdateCourtsForm(ModelForm):
    class Meta:
        model = Court
        fields = ['name', 'image_url']











