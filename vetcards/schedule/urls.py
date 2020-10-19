from django.urls import path, re_path
from django.urls import include
from .views import (create_slot, remove_slot, appoint_to_slot, 
disappoint_from_slot, vet_day_slots_list, vet_int_slots_list, day_slots_list, int_slots_list, pet_slots_list)

urlpatterns = [
    path('create', create_slot, name='create_slot'),
    path('delete', remove_slot, name='remove_slot'),
    path('appoint', appoint_to_slot, name='appoint_to_slot'),
    path('disappoint', disappoint_from_slot, name='disappoint_from_slot'),
    path('vet_day_sched', vet_day_slots_list, name='vet_day_slot_list'),
    path('vet_int_sched', vet_int_slots_list, name='vet_int_slot_list'),
    path('day_sched', day_slots_list, name='day_slot_list'),
    path('int_sched', int_slots_list, name='int_slot_list'),
    path('pet_sched', int_slots_list, name='pet_slot_list'),
]