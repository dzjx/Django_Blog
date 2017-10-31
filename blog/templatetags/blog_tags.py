#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : blog_tags.py
# @Author: Pen
# @Date  : 2017-10-30 13:42
# @Desc  : 自定义tags

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter, truncatechars_html
from django.urls import reverse
from Django_Blog.utils import logger
import blog.models as bm
import comments.models as cm

from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def datetime_format(date):
    try:
        return date.strftime(settings.DATE_TIME_FORMAT)
    except:
        return ""


@register.inclusion_tag('blog/tags/article_metas_info.html')
def load_article_metas(article, user):
    """
    文章元数据
    :param article:
    :param user:
    :return:
    """
    return {
        'article': article,
        'user': user
    }


@register.inclusion_tag('blog/tags/breadcrumb.html')
def load_breadcrumb(article):
    """
    获得文章面包屑
    :param article:
    :return:
    """

    names = article.get_category_tree()
    names.append((settings.SITE_NAME, settings.SITE_URL))
    names = names[::-1]  # 反转顺序

    return {
        'names': names,
        'title': article.title
    }


@register.inclusion_tag('blog/tags/article_info.html')
def load_article_detail(article, is_index, user):
    """
    加载文章详情
    :param article: 文章实体
    :param is_index: 是否列表页
    :param user: 当前用户
    :return:
    """

    return {
        'article': article,
        'is_index': is_index,
        'user': user
    }


@register.inclusion_tag('blog/tags/article_pagination.html')
def load_pagination_info(page_obj, page_type, tag_name):
    previous_url = ''
    next_url = ''
    if page_type == '':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:index_page', kwargs={'page': next_number})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:index_page', kwargs={'page': previous_number})
    if page_type == '分类标签归档':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:tag_detail_page', kwargs={'page': next_number, 'tag_name': tag_name})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:tag_detail_page', kwargs={'page': previous_number, 'tag_name': tag_name})
    if page_type == '作者文章归档':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:author_detail_page', kwargs={'page': next_number, 'author_name': tag_name})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:author_detail_page', kwargs={'page': previous_number, 'author_name': tag_name})

    if page_type == '分类目录归档':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:category_detail_page', kwargs={'page': next_number, 'category_name': tag_name})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:category_detail_page',
                                   kwargs={'page': previous_number, 'category_name': tag_name})

    return {
        'previous_url': previous_url,
        'next_url': next_url,
        'page_obj': page_obj
    }


@register.inclusion_tag('blog/tags/sidebar.html')
def load_sidebar(user):
    """
    加载侧边栏
    :return:
    """
    logger.info('load sidebar')
    recent_articles = bm.Article.objects.filter(status=2)[:settings.SIDEBAR_ARTICLE_COUNT]
    sidebar_categorys = bm.Category.objects.all()
    most_read_articles = bm.Article.objects.filter(status=2).order_by('-views')[:settings.SIDEBAR_ARTICLE_COUNT]
    dates = bm.Article.objects.datetimes('created_time', 'month', order='DESC')
    links = bm.Link.objects.all()
    commment_list = cm.Comment.objects.order_by('-id')[:settings.SIDEBAR_COMMENT_COUNT]
    show_adsense = settings.SHOW_GOOGLE_ADSENSE
    # 标签云 计算字体大小
    # 根据总数计算出平均值 大小为 (数目/平均值)*步长
    increment = 5
    tags = bm.Tag.objects.all()
    sidebar_tags = None
    if tags:
        s = list(map(lambda t: (t, t.get_article_count()), tags))
        count = sum(map(lambda t: t[1], s))
        dd = count / len(tags)
        sidebar_tags = list(map(lambda x: (x[0], x[1], (x[1] / dd) * increment + 10), s))

    return {
        'recent_articles': recent_articles,
        'sidebar_categorys': sidebar_categorys,
        'most_read_articles': most_read_articles,
        'article_dates': dates,
        'sidabar_links': links,
        'sidebar_comments': commment_list,
        'user': user,
        'show_adsense': show_adsense,
        'sidebar_tags': sidebar_tags
    }


@register.assignment_tag
def query(data, **kwargs):
    """
    eg:
    {% query books author=author as mybooks %}
    {% for book in mybooks %}
    ....
    {% endfor %}
    :param data: 数据集
    :param kwargs: 筛选参数
    :return:
    """

    return data.filter(**kwargs)


@register.filter(is_safe=True)
@stringfilter
def custom_markdown(content):
    from Django_Blog.utils import CommonMarkdown
    return mark_safe(CommonMarkdown.get_markdown(content))


@register.filter(is_safe=True)
@stringfilter
def truncatechars_content(content):
    """
    获得文章内容的摘要
    :param content:
    :return:
    """
    return truncatechars_html(content, settings.ARTICLE_SUB_LENGTH)
