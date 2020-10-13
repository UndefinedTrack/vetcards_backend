from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['user', 'name', 'species', 'breed', 'color', 'birth_date',
                   'gender', 'chip']


class PetUpdateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['id', 'user', 'name', 'species', 'breed', 'color', 'birth_date',
                   'gender', 'chip']