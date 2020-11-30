from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['user', 'name', 'species', 'breed', 'color', 'birth_date',
                   'gender', 'chip']


class PetUpdateForm(forms.ModelForm):
    
    pk = forms.IntegerField()
    class Meta:
        model = Pet
        fields = ['user', 'name', 'species', 'breed', 'color', 'birth_date',
                  'gender', 'chip', 'sterilized', 'vaccinated', 'contraindications', 
                  'notes', 'weight']
        

class PetAvatarForm(forms.Form):
    
    pk = forms.IntegerField()
    user = forms.IntegerField()
    avatar = forms.ImageField()
