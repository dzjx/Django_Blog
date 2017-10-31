#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : middleware.py
# @Author: Pen
# @Date  : 2017-10-30 17:00
# @Desc  : 自定义中间件

import time

from django.utils.deprecation import MiddlewareMixin
from ipware.ip import get_real_ip
from Django_Blog.utils import cache


class OnlineMiddleware(MiddlewareMixin):
    def process_request(self, request):
        self.start_time = time.time()

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        处理当前在线人数
        :param request:
        :param view_func:
        :param view_args:
        :param view_kwargs:
        :return:
        """
        online_ips = cache.get("online_ips", [])
        if online_ips:
            online_ips = cache.get_many(online_ips).keys()  # 获取还存在的ip
            online_ips = list(online_ips)

        ip = get_real_ip(request)
        cache.set(ip, 0, 5 * 60)  # 有效期5 分钟

        if ip not in online_ips:
            online_ips.append(ip)
            cache.set("online_ips", online_ips)

    def process_response(self, request, response):
        cast_time = 0.001
        if self.__dict__ and 'start_time' in self.__dict__:
            cast_time = time.time() - self.start_time
        response.content = response.content.replace(b'<!!LOAD_TIMES!!>', str.encode(str(cast_time)[:5]))
        return response
