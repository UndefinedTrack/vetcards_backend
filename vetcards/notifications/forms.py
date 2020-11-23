from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['pet', 'user', 'notif_type', 'description', 'repeat']

class UpdateNotificationForm(forms.ModelForm):

    pk = forms.IntegerField()
    class Meta:
        model = Notification
        fields = ['notif_type', 'description', 'repeat']