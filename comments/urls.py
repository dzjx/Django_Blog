#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Pen
# @Date  : 2017-11-02 13:33
# @Desc  :

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^article/(?P<article_id>\d+)/post_comment$', views.CommentPostView.as_view(), name='post_comment')
]
