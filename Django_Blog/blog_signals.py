#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : blog_signals.py
# @Author: Pen
# @Date  : 2017-11-03 11:45
# @Desc  :

from django.dispatch import receiver, Signal

# 相当于.net 中的事件
# 当评论后 在其他的app 中需要有后续操作时 各个app中只需要注册comment_save_signal这个信号就可以了,从而达到解耦
comment_save_signal = Signal(providing_args=['server_port', 'username', 'comment_id'])


@receiver(comment_save_signal)  # 相当于.net 中的注册事件
def send_comment_save_msg(sender, **kwargs):
    """
    保存评论成功后  eg : 这是要在通知app处理的逻辑
    :param sender:
    :param kwargs:
    :return:
    """
    print('发邮件')


@receiver(comment_save_signal)
def send_comment_save_log(sender, **kwargs):
    """
    保存评论成功后  eg : 这是要在日志app处理的逻辑
    :param sender:
    :param kwargs:
    :return:
    """

    print('记日志')
