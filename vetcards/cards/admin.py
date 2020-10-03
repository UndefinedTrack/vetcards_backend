from django.contrib import admin
from .models import Procedure, OwnerProcedure

# Register your models here.

class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet_id', 'purpose']
    
class OwnerProcedureAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet_id', 'user_id', 'name']
    

admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(OwnerProcedure, OwnerProcedureAdmin)
