from django.db import models
from authentication.models import UserProfile
from post.models import Blog
# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    notification_page = models.ManyToManyField(Blog,related_name='notification_page',blank = True)

    def __str__(self):
        return self.user.user.username