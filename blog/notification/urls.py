from django.urls import path
from . import views

app_name="notification"

urlpatterns = [
    path('<int:id>', views.notification_page,name="notification_page"),
    path('remove/<int:pk>', views.remove_notification,name="remove_notification"),
]