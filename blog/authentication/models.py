from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) #created when the object is first created
    updated_at = models.DateTimeField(auto_now=True) #updates when the model is updated
    following = models.ManyToManyField(User,related_name='following',blank = True)
    bookmarks = models.ManyToManyField('post.Blog',related_name='bookmarks',blank = True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank = True)
    
    def __str__(self):
        return self.user.username