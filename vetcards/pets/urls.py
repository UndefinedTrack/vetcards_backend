from django.urls import path, re_path
from django.urls import include
from .views import (create_pet, update_pet_info, delete_pet, pets_list, pet_info, patients_list, protected_file, upload_pet_avatar, search)

urlpatterns = [
    re_path(r'^avatars/.+$', protected_file, name="protected_file"),
    path('create', create_pet, name='create_pet'),
    path('update', update_pet_info, name='update_pet'),
    path('delete', delete_pet, name='delete_pet'),
    path('list', pets_list, name='pets_list'),
    path('info', pet_info, name='pet_info'),
    path('patients', patients_list, name='patients_list'),
    path('avatar', upload_pet_avatar, name='upload_pet_avatar'),
    path('search', search, name='search'),
]