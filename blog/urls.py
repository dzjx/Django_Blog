#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Pen
# @Date  : 2017-10-17 11:50
# @Desc  :
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'index_page/(?P<page>\d+)', views.IndexView.as_view(), name='index_page'),

    url(r'^article/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+).html$',
        views.ArticleDetailView.as_view(),
        name='detail'),
    url(r'^category/(?P<category_name>.*).html$', views.CategoryDetailView.as_view(), name='category')
]
