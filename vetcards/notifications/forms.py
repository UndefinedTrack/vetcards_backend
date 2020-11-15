from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['pet', 'user', 'notif_type', 'description', 'repeat']