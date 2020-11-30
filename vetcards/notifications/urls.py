from django.urls import path, re_path
from django.urls import include
from .views import (create_notification, delete_notification, notifications_list, update_notification, broadcast, contact)

urlpatterns = [
    path('broadcast', broadcast, name='broadcast'),
    path('create', create_notification, name='create_notification'),
    path('contact', contact, name='contact'),
    path('update', update_notification, name='update_notification'),
    path('delete', delete_notification, name='delete_notification'),
    path('list', notifications_list, name='notifications_list'),
]