from django.urls import path
from. import views

app_name = "post"

urlpatterns = [
    path('create_blog/', views.create_blog, name="create_blog"),
    path('<int:pk>/', views.personal_blog, name="personal_blog"),
    path('read/<int:pk>/', views.read_blog, name="read_blog"),
    path('edit/<int:pk>/', views.edit_blog, name="edit_blog"),
    path('delete/<int:pk>/', views.delete_blog, name="delete_blog"),
    path('latest_blogs/', views.latest_blogs, name="latest_blogs"),
    path('top_blogs/', views.top_blogs, name="top_blogs"),
]