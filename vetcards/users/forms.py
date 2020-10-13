from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'patronymic',
                   'last_name', 'phone', 'email']
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'patronymic',
                   'last_name', 'phone', 'email']