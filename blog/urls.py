#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Pen
# @Date  : 2017-10-17 11:50
# @Desc  :
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.IndexView.as_view()),
]
