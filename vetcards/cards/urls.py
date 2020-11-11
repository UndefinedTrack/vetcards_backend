from django.urls import path, re_path
from django.urls import include
from .views import (create_vet_procedure, create_owner_procedure, vet_procs_list, 
                    owner_procs_list, search_vet_procs, search_owner_procs, 
                    delete_vet_procedure, delete_owner_procedure, update_vet_procedure, update_owner_procedure)

urlpatterns = [
    path('create_vet', create_vet_procedure, name='create_vet'),
    path('create_owner', create_owner_procedure, name='create_owner'),
    path('get_vet', vet_procs_list, name='get_vet'),
    path('get_owner', owner_procs_list, name='get_owner'),
    path('delete_vet', delete_vet_procedure, name='delete_vet'),
    path('delete_owner', delete_owner_procedure, name='delete_owner'),
    path('update_vet', update_vet_procedure, name='update_vet'),
    path('update_owner', update_owner_procedure, name='update_owner'),
    path('search_vet_procs', search_vet_procs, name='search_vet_procs'),
    path('search_owner_procs', search_owner_procs, name='search_owner_procs')
]