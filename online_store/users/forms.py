from cProfile import label
import email
from re import L
from attr import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .bulma_mixin import BulmaMixin



class SignUpForm(BulmaMixin, UserCreationForm):
    username = forms.CharField(label='Create any username')
    email = forms.EmailField(label='Enter your email adress')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Create secure password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SignInForm(BulmaMixin, AuthenticationForm):
    username = forms.CharField(label='Enter username')
    password = forms.CharField(widget=forms.PasswordInput(),label='Enter password')


    class Meta:
        model = User
        fields = ['username', 'password']

class EditProfileForm(BulmaMixin, forms.ModelForm):
    email = forms.EmailField(label='Write your email')
    first_name = forms.CharField(label='Edit your first name')
    last_name = forms.CharField(label='Edit your last name')
    username = forms.CharField(label='Edit your username')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username']
        

class PasswordResetForm(BulmaMixin, PasswordChangeForm):
    old_password = forms.PasswordInput()
    new_password1 = forms.PasswordInput()
    new_password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

