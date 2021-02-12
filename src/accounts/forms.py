from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(
        attrs={
            'class':'form-control mb-2',
            'placeholder':'ПОЧТА'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control mb-2',
            'placeholder':'ПАРОЛЬ'
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'ПОДТВЕРДИТЕ ПАРОЛЬ'
        }))
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(
        attrs={
            'class':'form-control mb-2',
            'placeholder':'ПОЧТА'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control mb-2',
            'placeholder':'ПАРОЛЬ'
        }))

class TwoFactorForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control mb-2',
            'placeholder':'0000000000',
            'pattern':"^[0-9]{10}$"
        }
    ))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(
        attrs={
            'class':'form-control mb-2',
            'placeholder':'ПОЧТА'
        }
    ))

    class Meta:
        model = get_user_model()
        fields = ('email',  'first_name', 'second_name', 'bio')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']