from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'patronymic',
                   'last_name', 'phone', 'vet', 'avatar']
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'patronymic',
                   'last_name', 'phone', 'avatar']