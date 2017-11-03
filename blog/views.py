from django.conf import settings
from django import forms
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import generic

from Django_Blog import utils
from blog import models as bm
from blog.models import Article
from comments.forms import CommentForm


class ArticleListView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    page_kwarg = 'page'
    paginate_by = settings.PAGINATE_BY

    @property
    def page_number(self):
        return self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1

    def get_queryset(self):
        key = self.get_queryset_cache_key()
        value = utils.cache.get(key)

        if value:
            utils.logger.info('获取缓存值 key： {0}'.format(key))
        else:
            value = self.get_queryset_data()
            utils.cache.set(key, value, timeout=60 * 5)  # 缓存5 分钟
            utils.logger.info('设置缓存值 key： {0}'.format(key))

        return value

    def get_queryset_cache_key(self):
        raise NotImplementedError()

    def get_queryset_data(self):
        raise NotImplementedError()


class IndexView(ArticleListView):
    def get_queryset_cache_key(self):
        return 'index_{0}'.format(self.page_number)

    def get_queryset_data(self):
        return bm.Article.objects.filter(type=bm.Article.TYPE[0][0], status=bm.Article.STATUS_CHOICES[1][0]).order_by(
            '-pub_time')


class ArticleDetailView(generic.DetailView):
    template_name = 'blog/detail.html'
    model = Article
    context_object_name = "article"

    def get_object(self, queryset=None):
        """
        添加浏览次数
        :param queryset:
        :return:
        """
        self.object = super(ArticleDetailView, self).get_object(queryset)
        self.object.viewed()
        return self.object

    def get_context_data(self, **kwargs):
        comment_form = CommentForm()

        if self.request.user.is_authenticated and not self.request.user.is_anonymous:
            comment_form.fields.update({
                'email': forms.CharField(widget=forms.HiddenInput()),
                'name': forms.CharField(widget=forms.HiddenInput()),
            })
            comment_form.fields["email"].initial = self.request.user.email
            comment_form.fields["name"].initial = self.request.user.username

        article_comments = self.object.comment_set.all()

        kwargs['next_article'] = self.object.next_article
        kwargs['prev_article'] = self.object.prev_article
        kwargs['form'] = comment_form
        kwargs['article_comments'] = article_comments
        kwargs['comment_count'] = len(article_comments) if article_comments else 0

        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryDetailView(generic.DetailView):
    pass
