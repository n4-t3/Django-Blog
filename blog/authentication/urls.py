from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('signup/', views.signup_page,name='signup_page'),
    path('login/', views.login_page,name='login_page'),
    path('logout/', views.logout_page,name='logout_page'),
    path('profile/<int:pk>/', views.profile_page,name='profile_page'),
    path('edit/<int:pk>/', views.edit_user,name='edit_user'),
    path('delete/<int:pk>/', views.delete_user,name='delete_user'),
    path('', views.home_page,name='home_page'),
]
