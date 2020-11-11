from django import forms
from .models import Procedure, OwnerProcedure

class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = ['pet', 'user', 'purpose', 'symptoms', 
                  'diagnosis', 'recomms', 'recipe', 'proc_date']

class UpdateProcedureForm(forms.ModelForm):

    pk = forms.IntegerField()
    class Meta:
        model = Procedure
        fields = ['user', 'purpose', 'symptoms', 
                  'diagnosis', 'recomms', 'recipe', 'proc_date']
        
class OwnerProcedureForm(forms.ModelForm):
    class Meta:
        model = OwnerProcedure
        fields = ['pet', 'user', 'name', 'description', 'proc_date']


class UpdateOwnerProcedureForm(forms.ModelForm):

    pk = forms.IntegerField()
    class Meta:
        model = OwnerProcedure
        fields = ['user', 'name', 'description', 'proc_date']