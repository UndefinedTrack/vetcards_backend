from django.contrib import admin
from .models import Slot

# Register your models here.

class SlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'vet_id', 'pet_id', 'purpose']
    

admin.site.register(Slot, SlotAdmin)