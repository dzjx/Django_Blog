#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: Pen
# @Date  : 2017-11-01 10:45
# @Desc  :

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import widgets
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'placeholder': "username", "class": "form-control"})
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': "repeat password", "class": "form-control"})

    class Meta:
        model = get_user_model()
        fields = ('username',)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'placeholder': "username", "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})



