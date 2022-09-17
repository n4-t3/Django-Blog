from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django import forms
from .forms import UserCreationForm,UserCreationDate
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def home_page(request):
    return render(request,'index.html',context={})

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
            if 'profile_pic' in request.FILES:
                pre_save_time.profile_pic = request.FILES['profile_pic']
            pre_save_time.save()
            return HttpResponseRedirect(reverse('authentication:home_page'))
        else:
            if created_form.errors:
                for field1 in created_form.errors.as_data():
                    for error1 in created_form.errors.as_data()[field1]:
                        messages.error(request,f"{field1} {error1}")
            if time_form.errors:
                for field2 in time_form.errors.as_data():
                    for error2 in created_form.errors.as_data()[field2]:
                        messages.error(request,f"{field2} {error2}")
            return redirect("authentication:signup_page")
    return render(request,'authentication/signup.html',context=my_dict)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('authentication:home_page'))
            else:
                return HttpResponse('ACCOUNT IS NOT ACTIVE!')
        else:
            messages.error(request,"Invalid username or password")
            return redirect("authentication:login_page")
    return render(request,'authentication/login.html',context={})

@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:home_page'))