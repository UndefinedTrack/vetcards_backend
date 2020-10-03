from django.urls import path, re_path
from django.urls import include
from .views import (create_user, update_user_info, get_user_info)

urlpatterns = [
    path('create', create_user, name='create_user'),
    path('update', update_user_info, name='update_user'),
    path('info', get_user_info, name='get_user_info')
]