#from django.forms import ModelForm
from .models import Admin, Members
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password

class Adminform(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(Adminform, self).clean()
        post_email = cleaned_data['email']
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if (Admin.objects.filter(email= post_email).exists()):
            raise forms.ValidationError('Email already exists')
        if password!= password2:
            raise forms.ValidationError('Passwords do not match')

class MemberForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField() # Validators should be a list
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(MemberForm, self).clean()
        post_email = cleaned_data['email']
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if (Members.objects.filter(email= post_email).exists()):
            raise forms.ValidationError('Email already exists')
        if password!= password2:
            raise forms.ValidationError('Passwords do not match')
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean(self):
    #     cleaned_data = super(AdminLoginForm, self).clean()
    #     email = cleaned_data.get('email')
    #     password = cleaned_data.get('password')

        # if not Admin.objects.filter(email= email).exists():
        #     raise forms.ValidationError('Email does not exist')
        # if not Admin.objects.filter(email= email).first().check_password(password):
        #     raise forms.ValidationError('Password is incorrect')

