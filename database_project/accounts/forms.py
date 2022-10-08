from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
import datetime


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', required=True, min_length=4, max_length=255, widget=forms.TextInput(attrs={'class': 'input-form form-large'}))
    first_name = forms.CharField(label='Имя', required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'input-form form-large'}))
    password1 = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput(attrs={'class': 'input-form form-large', 'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Повторите пароль', required=True, widget=forms.PasswordInput(attrs={'class': 'input-form form-large', 'autocomplete': 'new-password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'input-form form-large', 'autofocus': True}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input-form form-large', 'autocomplete': 'current-password'}))


class SendImageForm(forms.Form):
    image_path = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*'}))


class SendVideoForm(forms.Form):
    video_path = forms.FileField(widget=forms.FileInput(attrs={'accept': 'video/*'}))
