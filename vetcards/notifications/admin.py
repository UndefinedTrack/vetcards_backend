from django.contrib import admin
from .models import Notification

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet_id', 'user_id', 'description']
    

admin.site.register(Notification, NotificationAdmin)