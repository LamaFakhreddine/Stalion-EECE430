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

class EnrollProgram(ModelForm):
    class Meta:
        model = MemberPrograms
        fields = ['program']

class EnrollProgram1(forms.Form):
    name = forms.CharField()

# class ReserveField(ModelForm):
#     class Meta:
#         model = CourtReservations
#         fields = ['court']

# class ReserveField1(forms.Form):
#     name = forms.CharField()



