from django.urls import path
from. import views

app_name = "post"

urlpatterns = [
    path('create_blog/', views.create_blog, name="create_blog"),
    path('<int:pk>/', views.personal_blog, name="personal_blog"),
    path('read/<int:pk>/', views.read_blog, name="read_blog"),
]