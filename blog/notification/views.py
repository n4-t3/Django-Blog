from django.shortcuts import render,redirect
from post.models import Blog
from authentication.models import UserProfile
from .models import Notification
from django.contrib.auth.models import User
# Create your views here.

def notification_page(request,id):
    user = User.objects.get(pk=id)
    user_profile = UserProfile.objects.get(user=user)
    try:
        notification = Notification.objects.get(user=user_profile)
    except:
        notification = Notification()
        notification.user=user_profile
        notification.save()
    notice = notification.notification_page.all()
    my_dict={
        'notification':notice
    }
    return render(request,'notification/notification_page.html',context=my_dict)

def remove_notification(request,pk):
    blog = Blog.objects.get(pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    notification = Notification.objects.get(user=user_profile)
    notification.notification_page.remove(blog)
    return redirect("post:read_blog",pk=pk)