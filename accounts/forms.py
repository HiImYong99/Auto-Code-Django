from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.hashers import check_password
from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1',
                  'password2', 'nickname', 'profile_pic']


class ChangeUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['nickname', 'profile_pic']
