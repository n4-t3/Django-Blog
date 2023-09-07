from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render,redirect
from .forms import UserCreationForm,UserCreationDate
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from post.models import Comment,Blog
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from notification.models import Notification
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
            return HttpResponseRedirect(reverse('authentication:login_page'))
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
    following = user.following.all()
    bookmarks = user.bookmarks.all()
    followers = user.followers.all()
    my_dict={
        'username':user.user.username,
        'image_path': user.profile_pic.name,
        'email': user.user.email,
        'followers':followers,
        'following': following,
        'bookmarks':bookmarks,
    }
    if not user.profile_pic.name:
        my_dict['image_path'] = "/profile_pics/default.jpg"
    return render(request,'authentication/profile.html',context=my_dict)

@login_required
def delete_user(request,pk):
    user = User.objects.get(pk=pk)
    if str(request.user) != str(user):
        return HttpResponseForbidden('Access Restricted!')
    user_profile = UserProfile.objects.get(user=user)
    blogs = Blog.objects.filter(author=user_profile)
    comments = Comment.objects.filter(comment_author=user_profile)
    notification = Notification.objects.filter(user=user_profile)
    for notice in notification:
        notice.delete()
    for comment in comments:
        comment.delete()
    for blog in blogs:
        for ip in blog.views.all():
            ip.delete()
        blog.delete()
    user_profile.delete()
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

def remove_following(request,pk):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(user=user)
        following_user = User.objects.get(pk=pk)
        following_user_profile = UserProfile.objects.get(user=following_user)
        if len(UserProfile.objects.filter(following__username=user_profile.user.username))!=0:
            user_profile.following.remove(following_user)
            following_user_profile.followers.remove(user)
            messages.info(request,f"Unfollowed {following_user.username}")
        else:
            messages.warning(request,"Something went wrong!")
    else:
        return HttpResponseForbidden("Access Restricted!")
    return redirect("authentication:profile_page",pk=user.id)

def remove_follower(request,pk):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(user=user)
        follower_user = User.objects.get(pk=pk)
        follower_user_profile = UserProfile.objects.get(user=follower_user)
        if len(UserProfile.objects.filter(followers__username=user_profile.user.username))!=0:
            user_profile.followers.remove(follower_user)
            follower_user_profile.following.remove(user)
            messages.info(request,f"Removed {follower_user.username}")
        else:
            messages.warning(request,"Something went wrong!")
    else:
        return HttpResponseForbidden("Access Restricted!")
    return redirect("authentication:profile_page",pk=user.id)

def search_following_blog(request,pk):
    following_profile = User.objects.get(pk=pk)
    following_user_profile = UserProfile.objects.get(user=following_profile)
    pagination = Paginator(Blog.objects.filter(author=following_user_profile).order_by('-posted_date'),per_page=6)
    try:
        current_page = int(request.GET.get('page',1))
    except:
        messages.error(request,"Page not found!")
        return redirect("post:latest_blogs")
    page_obj = pagination.get_page(current_page)
    page = pagination.page(current_page)
    my_dict = {
        "blogs":page_obj,
        "number_of_pages": pagination.num_pages,
        "pagination" : pagination,
        "page_has_next":page.has_next(),
        "page_has_previous":page.has_previous(),
        "current_page":current_page, 
        "page_range": pagination.get_elided_page_range(current_page, on_each_side=3, on_ends=2)
    }
    return render(request,'post/latest_blogs.html',context=my_dict)