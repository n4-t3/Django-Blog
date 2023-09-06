from . import models
from django import forms

class CreateBlog(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ["category","blog_title","blog_body","summary","cover_image"]

class CreateComment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ["blog_comment"]