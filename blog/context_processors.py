#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : context_processors.py
# @Author: Pen
# @Date  : 2017-10-31 11:38
# @Desc  : 扩展上下文
from django.conf import settings
from Django_Blog.utils import logger, cache
from blog.models import Category, Article


def seo_processors(requests):
    key = 'seo_processors'
    value = cache.get(key)

    if value:
        logger.info('get seo_processors value')
        return value
    else:
        logger.info('set seo_processors value')
        value = {
            'SITE_NAME': settings.SITE_NAME,
            'SHOW_GOOGLE_ADSENSE': settings.SHOW_GOOGLE_ADSENSE,
            'SITE_SEO_DESCRIPTION': settings.SITE_SEO_DESCRIPTION,
            'SITE_DESCRIPTION': settings.SITE_DESCRIPTION,
            'SITE_KEYWORDS': settings.SITE_SEO_KEYWORDS,
            'SITE_BASE_URL': requests.scheme + '://' + requests.get_host() + '/',
            'ARTICLE_SUB_LENGTH': settings.ARTICLE_SUB_LENGTH,

            'nav_category_list': Category.objects.all(),
            'nav_pages': Article.objects.filter(type=2, status=2),  # 放在导航上面的文章
        }

        cache.set(key, value, 60 * 60 * 10)
        return value
