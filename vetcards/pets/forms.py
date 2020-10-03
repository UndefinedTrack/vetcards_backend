from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['user', 'name', 'species', 'color', 'birth_date',
                   'gender', 'chip']