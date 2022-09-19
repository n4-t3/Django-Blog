from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse
from .forms import CreateBlog,CreateComment
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile
from django.contrib.auth.models import User
from . import models
from django.contrib import messages
from django.core.paginator import Paginator
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
    blogs = models.Blog.objects.filter(author=author)
    pagination = Paginator(blogs,per_page=6)
    try:
        current_page = int(request.GET.get('page',1))
    except:
        messages.error(request,"Page not found!")
        return redirect("post:personal_blog", pk=pk)
    page_obj = pagination.get_page(current_page)
    page = pagination.page(current_page)
    my_dict = {
        "blogs":page_obj,
        "create_comment":CreateComment,
        "number_of_pages": pagination.num_pages,
        "pagination" : pagination,
        "page_has_next":page.has_next(),
        "page_has_previous":page.has_previous(),
        "current_page":current_page, 
        "page_range": pagination.get_elided_page_range(current_page, on_each_side=3, on_ends=2)
    }
    return render(request,'post/my_blog.html',context=my_dict)

def read_blog(request,pk):
    blog = models.Blog.objects.get(pk =pk)
    user = UserProfile.objects.get(user=request.user)
    main_user = request.user
    my_dict = {
        "blog":blog,
        "comments": models.Comment.objects.filter(blog=blog).order_by("-post_date"),
        "user_profile": main_user,
        "is_blog_author":False,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            user = UserProfile.objects.get(user=request.user)
            if request.POST.get("like"):
                if user in blog.likes.all():
                    blog.likes.remove(user)
                    messages.warning(request,"Unliked the post!")
                    return redirect("post:read_blog",pk=pk)
                else:
                    blog.likes.add(user)
                    blog.save()
                    messages.success(request,"Liked the post!")
                    return redirect("post:read_blog",pk=pk)
            if request.POST.get("comment"):
                if request.user == blog.author:
                    my_dict['is_blog_author'] =True
                comment = request.POST.get("user_comment")
                comment_form = CreateComment().save(commit=False)
                comment_form.comment_author = user
                comment_form.blog = blog
                comment_form.blog_comment = comment
                comment_form.save()
                return redirect("post:read_blog",pk=pk)
        else:
            messages.info(request,"Login to like or comment on the post!")
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

def top_blogs(request):
    pagination = Paginator(models.Blog.objects.all().order_by('-likes'),per_page=4)
    try:
        current_page = int(request.GET.get('page',1))
    except:
        messages.error(request,"Page not found!")
        return redirect("post:top_blog")
    page_obj = pagination.get_page(current_page)
    page = pagination.page(current_page)
    my_dict = {
        "blogs":page_obj,
        "create_comment":CreateComment,
        "number_of_pages": pagination.num_pages,
        "pagination" : pagination,
        "page_has_next":page.has_next(),
        "page_has_previous":page.has_previous(),
        "current_page":current_page, 
        "page_range": pagination.get_elided_page_range(current_page, on_each_side=3, on_ends=2)
    }
    return render(request,'post/top_blogs.html',context=my_dict)

def latest_blogs(request):
    pagination = Paginator(models.Blog.objects.all().order_by('-posted_date'),per_page=4)
    try:
        current_page = int(request.GET.get('page',1))
    except:
        messages.error(request,"Page not found!")
        return redirect("post:latest_blogs")
    page_obj = pagination.get_page(current_page)
    page = pagination.page(current_page)
    my_dict = {
        "blogs":page_obj,
        "create_comment":CreateComment,
        "number_of_pages": pagination.num_pages,
        "pagination" : pagination,
        "page_has_next":page.has_next(),
        "page_has_previous":page.has_previous(),
        "current_page":current_page, 
        "page_range": pagination.get_elided_page_range(current_page, on_each_side=3, on_ends=2)
    }
    return render(request,'post/latest_blogs.html',context=my_dict)