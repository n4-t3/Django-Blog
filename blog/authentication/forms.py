from django import forms
from django.contrib.auth.models import User
from . import models

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','password')

class UserCreationDate(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ["profile_pic"]
