from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render,redirect
from django import forms
from .forms import UserCreationForm,UserCreationDate
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User
# Create your views here.

def home_page(request):
    return render(request,'index.html',context={})

def signup_page(request):
    my_dict = {
        'signup_form' : UserCreationForm,
        'time_form':UserCreationDate,
        'purpose': "signup"
    }
    if request.method == "POST":
        created_form = UserCreationForm(request.POST)
        time_form = UserCreationDate(request.POST)
        if created_form.is_valid() and time_form.is_valid():
            pre_save_form = created_form.save()
            pre_save_form.set_password(pre_save_form.password)
            pre_save_form.save()
            pre_save_time = time_form.save(commit=False)
            user = User.objects.get(username = pre_save_form.username)
            pre_save_time.user = user
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

@login_required
def profile_page(request,pk):
    user = UserProfile.objects.get(user_id=pk)
    if str(request.user) != str(user.user.username):
        return HttpResponseForbidden('Access Restricted!')
    followers = user.followers
    bookmarks = user.bookmarks
    my_dict={
        'username':user.user.username,
        'image_path': user.profile_pic.name,
        'email': user.user.email,
        'followers': followers,
        'bookmarks':bookmarks
    }
    if not user.profile_pic.name:
        my_dict['image_path'] = "/profile_pics/default.jpg"
    return render(request,'authentication/profile.html',context=my_dict)

@login_required
def delete_user(request,pk):
    user = User.objects.get(pk=pk)
    if str(request.user) != str(user):
        return HttpResponseForbidden('Access Restricted!')
    user.delete()
    return HttpResponseRedirect(reverse('authentication:login_page'))

@login_required
def edit_user(request,pk):
    try:
        user = UserProfile.objects.get(user_id=pk)
    except UserProfile.DoesNotExist:
        return HttpResponse("invalid user profile!")
    if str(request.user) != str(user.user.username):
        return HttpResponseForbidden('Access Restricted!')
    user_form= UserCreationForm(instance = user.user)
    image_form= UserCreationDate(instance = user)
    my_dict={
        'user_form': user_form,
        'image_form': image_form,
        'purpose': "Edit Profile"
    }
    if request.method == "POST":
        sent_user_form = UserCreationForm(request.POST,instance = user.user)
        sent_image_form= UserCreationDate(request.POST,instance = user) 
        if sent_user_form.is_valid() and sent_image_form.is_valid():
            pre_save_user =  sent_user_form.save()
            pre_save_user.set_password(pre_save_user.password)
            pre_save_user.save()
            pre_save_image = sent_image_form.save(commit=False)
            pre_save_image.user = pre_save_user
            if 'profile_pic' in request.FILES:
                pre_save_image.profile_pic = request.FILES['profile_pic']
            pre_save_image.save()
            return HttpResponseRedirect(reverse('authentication:login_page'))
        else:
            if sent_user_form.errors:
                for field1 in sent_user_form.errors.as_data():
                    for error1 in sent_user_form.errors.as_data()[field1]:
                        messages.error(request,f"{field1} {error1}")
                return redirect('authentication:edit_user',pk=pk)
            if sent_image_form.errors:
                for field2 in sent_image_form.errors.as_data():
                    for error2 in sent_image_form.errors.as_data()[field2]:
                        messages.error(request,f"{field2} {error2}")
            return redirect('authentication:edit_user',pk=pk)
    return render(request,'authentication/edit_user.html',context=my_dict)