from django.shortcuts import render
from django.http import HttpResponse
from . import forms
# Create your views here.

def login_page(request):
    my_dict = {
        'login_form' : forms.UserCreationForm
    }
    return render(request,'authentication/login.html',context=my_dict)
