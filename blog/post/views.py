from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse
from .forms import CreateBlog,CreateComment
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from . import models
from django.contrib import messages
# Create your views here.


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
            if 'cover_image' in request.FILES:
                pre_save_blog.cover_image = request.FILES['cover_image']
            pre_save_blog.save()
            return HttpResponseRedirect(reverse('authentication:home_page'))
        else:
            if blog_form.errors:
                for field in blog_form.errors.as_data():
                    for error in blog_form.errors.as_data()[field]:
                        messages.error(request,f"{field} {error}")
            return redirect("post:create_blog")
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

def read_blog(request,pk):
    blog = models.Blog.objects.get(pk =pk)
    my_dict = {
        "blog":blog
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            user = UserProfile.objects.get(user=request.user)
            print('---------------------------------')
            print(blog.likes.all())
            if user in blog.likes.all():
                blog.likes.remove(user)
                messages.warning(request,"Unliked the post!")
                return redirect("post:read_blog",pk=pk)
            else:
                blog.likes.add(user)
                blog.save()
                messages.success(request,"Liked the post!")
                return redirect("post:read_blog",pk=pk)
        else:
            messages.info(request,"Login to like the post!")
            return redirect("post:read_blog",pk=pk)
    else:
        blog.views = blog.views + 1
        blog.save()
    return render(request,'post/read_blog.html',context=my_dict)

@login_required
def edit_blog(request,pk):
    blog = models.Blog.objects.get(id=pk)
    if str(request.user) != str(blog.author.user):
        return HttpResponseForbidden('Access Restricted!')
    form = CreateBlog(instance=blog)
    my_dict = {
        "create_blog": form
    }
    if request.method == "POST":
        blog_form = CreateBlog(request.POST,instance=blog)
        if blog_form.is_valid():
            pre_save_blog = blog_form.save(commit=False)
            user = User.objects.get(username = request.user.username)
            author = UserProfile.objects.get(user=user)
            pre_save_blog.author = author
            if 'cover_image' in request.FILES:
                pre_save_blog.cover_image = request.FILES['cover_image']
            pre_save_blog.save()
            return redirect("post:personal_blog", pk=user.id) 
        else:
            if blog_form.errors:
                for field in blog_form.errors.as_data():
                    for error in blog_form.errors.as_data()[field]:
                        messages.error(request,f"{field} {error}")
            return redirect("post:edit_blog", pk=pk)
    return render(request,"post/create_blog.html",context=my_dict)

@login_required
def delete_blog(request,pk):
    blog = models.Blog.objects.get(id=pk)
    if str(request.user) != str(blog.author.user):
        return HttpResponseForbidden('Access Restricted!')
    blog.delete()
    return redirect("post:personal_blog", pk=blog.author.user.id) 


def public_blog(request):
    my_dict={
        'top_posts':models.Blog.objects.all().order_by('-likes')[:5],
        'new_posts':models.Blog.objects.all().order_by('-updated_date')[:5]
    }
    return render(request,'post/public.html',context=my_dict) 