#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Pen
# @Date  : 2017-10-17 09:47
# @Desc  : 测试


import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_Blog.settings")

import Django_Blog.utils as uti


@uti.decorator_cache(60 * 60 * 10)
def cache_test(pra):
    return pra + 1


if __name__ == '__main__':
    assert uti.get_md5('123')
    assert isinstance(uti.get_md5('123'), str)

    cache_test(2)
