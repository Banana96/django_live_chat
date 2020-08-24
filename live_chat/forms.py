from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
