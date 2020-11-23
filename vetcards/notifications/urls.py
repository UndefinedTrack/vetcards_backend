from django.urls import path, re_path
from django.urls import include
from .views import (create_notification, delete_notification, notifications_list, update_notification)

urlpatterns = [
    path('create', create_notification, name='create_notification'),
    path('update', update_notification, name='update_notification'),
    path('delete', delete_notification, name='delete_notification'),
    path('list', notifications_list, name='notifications_list'),
]