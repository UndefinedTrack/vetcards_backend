from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'patronymic',
                   'last_name', 'phone', 'email']
        
class UpdateUserForm(forms.ModelForm):
    
    pk = forms.IntegerField()
    class Meta:
        model = User
        fields = ['first_name', 'patronymic',
                  'last_name', 'phone', 'email', 
                  'region', 'city', 'street',
                  'address', 'passport', 'paid_service']
        
class UserAvatarForm(forms.Form):
    
    pk = forms.IntegerField()
    avatar = forms.ImageField()