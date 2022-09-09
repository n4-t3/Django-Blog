from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from .forms import UserCreationForm,UserCreationDate
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def signup_page(request):
    my_dict = {
        'signup_form' : UserCreationForm,
        'time_form':UserCreationDate
    }
    if request.method == "POST":
        created_form = UserCreationForm(request.POST)
        time_form = UserCreationDate(request.POST)
        if created_form.is_valid() and time_form.is_valid():
            pre_save_form = created_form.save(commit=False)
            pre_save_form.set_password(request.POST.get('password'))
            pre_save_form.save()
            pre_save_time = time_form.save(commit=False)
            pre_save_time.user = pre_save_form
            pre_save_time.save()
        else:
            raise forms.ValidationError(('Something went wrong, try again!'),code= 'invalid')
            
    return render(request,'authentication/signup.html',context=my_dict)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
            else:
                HttpResponse('ACCOUNT IS NOT ACTIVE!')
        else:
            raise forms.ValidationError(('Something went wrong, try again!'),code= 'invalid')
            
    return render(request,'authentication/login.html')
