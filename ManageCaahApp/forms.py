from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from ManageCaahApp.models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    pass 

class UserModifyForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username' , 'email']

class AddCashForm(forms.ModelForm):
    class Meta:
        model = AddCash
        fields = '__all__'
        exclude = ['user']
        widgets={
            'datetime' : forms.DateTimeInput(attrs={
                'type': 'datetime-local',
            })
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseModel
        fields = '__all__'
        exclude = ['user']
        widgets={
            'datetime' : forms.DateTimeInput(attrs={
                'type': 'datetime-local',
            })
        }