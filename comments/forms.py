#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: Pen
# @Date  : 2017-11-02 15:31
# @Desc  :

from django.forms import ModelForm
from django import forms

from comments.models import Comment


class CommentForm(ModelForm):
    url = forms.URLField(label='网址', required=False)
    email = forms.EmailField(label='电子邮箱', required=True)
    name = forms.CharField(label='姓名', widget=forms.TextInput(attrs=
                                                              {'value': "", 'size': "30", 'maxlength': "245",
                                                               'aria-required': 'true'}
                                                              ))
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body']