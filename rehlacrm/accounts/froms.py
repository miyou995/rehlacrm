from django.core.mail import send_mail
import logging
from django.contrib import messages
from django.contrib.auth.forms import ( UserCreationForm as DjangoUserCreationForm )
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import authenticate
from . import models 

from django import forms

logger = logging.getLogger(__name__)

class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email": UsernameField}

class UserEditForm(forms.ModelForm):
    class Meta: 
        model = models.User
        fields = ("picture","pseudo", "role", "warehouse", "notes")
        required= ( "role", "warehouse",)


class UserAddForm(forms.ModelForm):
    my_user = forms.CharField()
    class Meta: 
        model = models.User
        fields = ("picture","role", "warehouse","notes", "is_manager","is_active","is_staff", "my_user")
        required= ( "warehouse", "role", )        
         
    #

class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
            strip=False, widget=forms.PasswordInput 
    )
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email is not None and password:
            self.user = authenticate(
                self.request, email=email, password=password
            )
            if self.user is None:
                raise forms.ValidationError(
                    "Invalid email/password combination."
            )
        logger.info(
            "Authentication successful for email=%s", email
            )
        return self.cleaned_data
    def get_user(self):
        return self.user 



class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = models.User
        fields = ('email' , 'password')
        widgets = {
            # 'first_name': forms.TextInput(attrs={'class' : 'form-control' }),
            'email'     : forms.EmailInput(attrs={'class' : 'form-control' }),
            'password'  : forms.PasswordInput(attrs={'class' : 'form-control' }),
        }

class ChangePasswordForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = models.User
        fields = ('password',)
        widgets = {
            # 'first_name': forms.TextInput(attrs={'class' : 'form-control' }),
            'password'  : forms.PasswordInput(attrs={'class' : 'form-control' }),
        }
