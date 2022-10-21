from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        exclude = ('geolocation', 'manager', 'visitors')


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = ('place', 'rating', 'rated_by')


class CommentForm(forms.Form):
    text = forms.CharField(label='comment', widget=forms.TextInput(attrs={'placeholder': 'here'}),
                           max_length=128)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('username', 'password2')
