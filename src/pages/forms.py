from django import forms
from django.core.exceptions import ValidationError

def validate_phone(value):
    if not value.is_digit():
        raise ValidationError('Введите корректный номер телефона')

class CompanyForm(forms.Form):
    location = forms.CharField(max_length=255, required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Москва'
        })
    ) 
    company = forms.CharField(max_length=255, required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'ООО"ЭЭЭ"'
        })
    ) 
    warehouse_size = forms.CharField(max_length=128, required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'10 Га'
        })
    )
    contact = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'+79991234567'
        }))

class PartnerForm(forms.Form):
    name = forms.CharField(max_length=128, required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Иванов Иван'
        })
    ) 
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'placeholder':'ivanov@ivan.com'
        })
    )
    message = forms.CharField(max_length=2000, required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Сообщение'
        }))

class CallMeForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'79991234567',
            'pattern':"^[\+]*[0-9]+$"
        }
    ))