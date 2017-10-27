#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: Pen
# @Date  : 2017-10-16 20:51
# @Desc  : 小工具集合

from hashlib import md5
from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)


def get_md5(source_str):
    """
    获取md5 字符串
    :param source_str: 源串
    :return:
    """
    m = md5(source_str.encode('utf-8'))

    return m.hexdigest()


def decorator_cache(time_out=None):
    """
    缓存装饰器
    :param time_out: 过期时间 默认不过期
    :return:
    """

    def wrap_func(func):
        def wrap(*args, **kwargs):
            try:
                view = args[0]
                key = view.get_cache_key()
            except (AttributeError, IndexError):
                key = None
                pass

            if not key:
                unique_str = repr((func.__name__, args, kwargs))
                key = get_md5(unique_str)

            value = cache.get(key)

            if value:
                logger.info('{0} 获取缓存值 key： {1}'.format(func.__name__, key))
                return value
            else:
                logger.info('{0} 设置缓存值 key： {1}'.format(func.__name__, key))
                value = func(*args, **kwargs)
                cache.set(key, value, time_out)
                return value

        return wrap

    return wrap_func
