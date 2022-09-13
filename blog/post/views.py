from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .forms import CreateBlog,CreateComment
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from . import models
# Create your views here.

def index(request):
    return HttpResponse('hi')

@login_required
def create_blog(request):
    my_dict = {
        "create_blog": CreateBlog
    }
    if request.method == "POST":
        blog_form = CreateBlog(request.POST)
        if blog_form.is_valid():
            pre_save_blog = blog_form.save(commit=False)
            user = User.objects.get(username = request.user.username)
            author = UserProfile.objects.get(user=user)
            pre_save_blog.author = author
            pre_save_blog.save()
            return HttpResponseRedirect(reverse('authentication:home_page'))
        else:
            raise forms.ValidationError("Something isn't right please try again!")
    return render(request,"post/create_blog.html",context=my_dict)

@login_required
def personal_blog(request,pk):
    user = User.objects.get(pk =pk)
    author = UserProfile.objects.get(user=user)
    my_dict = {
        "blogs":models.Blog.objects.filter(author=author),
        "create_comment":CreateComment
    }
    return render(request,'post/my_blog.html',context=my_dict)