from unicodedata import category
from django.db import models
from authentication.models import UserProfile
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
# Create your models here.

CATEGORY_CHOICES = ((1, 'Personal Blog'), (2, 'Business Blog'), (3, 'Technology Blog'), (4, 'Fashion Blog'),(5, 'Education Blog'), (6, 'Health and Fitness Blog'), (7, 'Food Blog'), (8, 'Sports Blog'), (9, 'Travel Blog'), (10, 'Lifestyle Blog'), (11, 'Photography Blog'), (12, 'Political Blog'), (13, 'Parenting Blog'), (14, 'Wedding Blog'), (15, 'Pet Blog'), (16, 'Home Décor Blog'),
(17, 'DIY Blog'), (18, 'Marketing Blog'), (19, 'Entrepreneur Blog'), (20, 'Gaming Blog'), (21, 'Science Blog'), (22, 'Review Blog'), (23, 'Finance Blog'), (24, 'Music Blog'), (25, 'Movie Blog'))


class IpAddress(models.Model):
    address = models.CharField(max_length=255)
    def __str__(self):
        return self.address

        
class Blog(models.Model):
    author=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # created when the object is first created
    posted_date=models.DateTimeField(auto_now_add=True)
    # updates when the model is updated
    updated_date=models.DateTimeField(auto_now=True)
    category=MultiSelectField(choices=CATEGORY_CHOICES,
                                 max_choices=4,
                                 max_length=100)
    blog_title=models.CharField(max_length=255, blank=False)
    blog_body=RichTextField(blank=False, null=False)
    summary=models.CharField(
        max_length=255, default="Summary was not provided :(")
    cover_image=models.ImageField(upload_to='covers', blank=True)
    likes=models.ManyToManyField(UserProfile, related_name='likers')
    views = models.ManyToManyField(IpAddress, related_name='views')

    def __str__(self):
        return self.blog_title

class Comment(models.Model):
    comment_author=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_date=models.DateField(auto_now_add=True)
    blog_comment=models.TextField(blank=False)

    def __str__(self):
        return self.blog_comment
