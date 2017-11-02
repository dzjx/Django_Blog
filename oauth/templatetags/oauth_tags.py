#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : oauth_tags.py
# @Author: Pen
# @Date  : 2017-11-01 15:05
# @Desc  :

from django import template

register = template.Library()


@register.inclusion_tag('oauth/oauth_applications.html')
def load_oauth_applications(request):
    pass
