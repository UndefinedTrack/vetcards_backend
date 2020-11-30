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

class BroadcastNotificationForm(forms.Form):

    region = forms.CharField(max_length=128)
    city = forms.CharField(max_length=128)
    street = forms.CharField(max_length=128)

    subject = forms.CharField(max_length=128)
    message = forms.CharField(max_length=512)

class ContactForm(forms.Form):
    last_name = forms.CharField(max_length=128)
    first_name = forms.CharField(max_length=128)
    email = forms.CharField(max_length=128)