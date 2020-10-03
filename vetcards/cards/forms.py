from django import forms
from .models import Procedure, OwnerProcedure

class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = ['pet', 'user', 'purpose', 'symptoms', 
                  'diagnosis', 'recomms', 'recipe']
        
class OwnerProcedureForm(forms.ModelForm):
    class Meta:
        model = OwnerProcedure
        fields = ['pet', 'user', 'name', 'description']