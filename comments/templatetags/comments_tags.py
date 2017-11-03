#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : comments_tags.py
# @Author: Pen
# @Date  : 2017-11-02 11:38
# @Desc  :

from  django import template

register = template.Library()


@register.inclusion_tag('comments/tags/comment_item.html')
def show_comment_item(comment, is_child):
    """
    显示评论详情
    :param comment:
    :param is_child:
    :return:
    """
    depth = 1 if is_child else 2

    return {'comment_item': comment, 'depth': depth}


@register.assignment_tag
def parse_comment_tree(comment_list, comment):
    """
    获取子评论列表
    :param comment_list:
    :param comment:
    :return:
    """

    data = []

    def parse(c):
        childs = comment_list.filter(parent_comment=c)
        for child in childs:
            data.append(child)
            parse(child)

    parse(comment)
    return data
