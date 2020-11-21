from django.urls import path, re_path
from django.urls import include
from .views import (create_user, update_user_info, get_user_info, csrf, vets_list, upload_user_avatar, protected_file, test)

urlpatterns = [
    re_path(r'^avatars/.+$', protected_file, name="protected_file"),
    path('create', create_user, name='create_user'),
    path('update', update_user_info, name='update_user'),
    path('info', get_user_info, name='get_user_info'),
    path('csrf', csrf, name='csrf'),
    path('vets', vets_list, name='vets'),
    path('avatar', upload_user_avatar, name='upload_user_avatar'),
    path('test', test, name='test')
]