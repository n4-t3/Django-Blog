from django import forms
from . import models
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','password')

class UserCreationDate(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = ('user','created_at','updated_at',)