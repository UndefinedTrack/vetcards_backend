from django import forms
from .models import Slot

class SlotCreateForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['vet', 'slot_date', 'slot_time']


class SlotAppointForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['id', 'purpose', 'pet']

class SlotDisappointForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['id', 'pet']