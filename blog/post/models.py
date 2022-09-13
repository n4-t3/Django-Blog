from unicodedata import category
from django.db import models
from authentication.models import UserProfile
from ckeditor.fields import RichTextField
# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True) #created when the object is first created
    updated_date = models.DateTimeField(auto_now=True) #updates when the model is updated
    category = models.CharField(max_length=255)
    blog_title = models.CharField(max_length=255,blank=False)
    blog_body = RichTextField(blank=False, null = False)
    likes = models.ManyToManyField(UserProfile,related_name='likers')

    def __str__(self):
        return self.blog_title

class Comment(models.Model):
    comment_author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    post_date = models.DateField(auto_now_add = True)
    blog_comment = models.TextField(blank=False)

    def __str__(self):
        return self.blog_comment
