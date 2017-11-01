from django.conf import settings
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import generic

from Django_Blog import utils
from blog import models as bm


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


class DetailView(generic.DetailView):
    pass

class CategoryDetailView(generic.DetailView):
    pass