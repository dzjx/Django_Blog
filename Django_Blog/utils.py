#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: Pen
# @Date  : 2017-10-16 20:51
# @Desc  : 小工具集合

from hashlib import md5

from django.core.cache import cache
import logging

import mistune
from mistune import escape, escape_link
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

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


def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )


class BlogMarkDownRenderer(mistune.Renderer):
    def block_code(self, text, lang):
        inlinestyles = self.options.get('inlinestyles')
        linenos = self.options.get('linenos')
        return block_code(text, lang, inlinestyles, linenos)

    def autolink(self, link, is_email=False):
        text = link = escape(link)

        if is_email:
            link = 'mailto:%s' % link
        if not link:
            link = "#"
        # site = Site.objects.get_current()
        # nofollow = "" if link.find(site.domain) > 0 else "rel='nofollow'"

        nofollow = "rel='nofollow'"
        return '<a href="%s" %s>%s</a>' % (link, nofollow, text)

    def link(self, link, title, text):
        link = escape_link(link)
        site = Site.objects.get_current()
        nofollow = "" if link.find(site.domain) > 0 else "rel='nofollow'"
        if not link:
            link = "#"
        if not title:
            return '<a href="%s" %s>%s</a>' % (link, nofollow, text)
        title = escape(title, quote=True)
        return '<a href="%s" title="%s" %s>%s</a>' % (link, title, nofollow, text)


class CommonMarkdown:
    @staticmethod
    def get_markdown(value):
        renderer = BlogMarkDownRenderer(inlinestyles=False)
        mdp = mistune.Markdown(escape=True, renderer=renderer)
        return mdp(value)
