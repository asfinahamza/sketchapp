from django import forms
from ckeditor.widgets import CKEditorWidget
from sketchapp.models import *



class LoginForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(
        max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))

