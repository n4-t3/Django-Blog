from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('signup/', views.signup_page,name='signup_page'),
    path('login/', views.login_page,name='login_page'),
    path('', views.home_page,name='home_page'),
]
