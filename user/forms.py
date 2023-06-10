from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
import datetime


class UserRegisterationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        # self.fields['is_teacher'].label = ''
        # self.fields['is_student'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter Password'
        # self.fields['is_teacher'].widget.attrs['class'] = 'Teacher'
        # self.fields['is_student'].widget.attrs['class'] = 'Student'

    password1 = forms.CharField(label='Enter password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)
    is_teacher = forms.BooleanField(label=("is Teacher?"),required=False)
    is_student = forms.BooleanField(label=("is Student?"),required=False)

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "email","is_teacher","is_student")
        help_texts = {
            "username": None,
        }

class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    password = forms.CharField(label='Enter password',
                               widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username", "password")
        help_texts = {
            "username": None,
        }