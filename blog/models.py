from django.db import models
from django.conf import settings
from django.urls import reverse

from Django_Blog import utils


class BaseModel(models.Model):
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('最后修改时间', auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # TODO

    class Meta:
        abstract = True


class Category(BaseModel):
    """
    文章分类
    """
    name = models.CharField('分类名称', max_length=30, unique=True)
    parent_category = models.ForeignKey('self', verbose_name='父级分类', blank=True, null=True)  # 默认级联删除

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'category_name': self.name})

    @property
    @utils.decorator_cache(60 * 60 * 5)  # 缓存5分钟
    def category_parent(self):
        """
        当前节点的所有父节点
        :return:
        """

        parents = []

        def parse(entry):
            parents.append(entry)
            if entry.parent_category:
                parse(entry.parent_category)

        parse(self)

        return parents

    @property
    @utils.decorator_cache(60 * 60 * 5)  # 缓存5分钟
    def category_child(self):
        """
        当前节点的所有子节点
        :return:
        """
        children_data = []
        category_all = Category.objects.all()

        def parse(category):
            for c in category_all:
                children_data.append(category)

                children_all = category_all.filter(parent_category=category)
                for children in children_all:
                    children_data.append(children)
                    parse(children)

        parse(self)

        children_data = list(set(children_data))

        return children_data

    class Meta:
        ordering = ['name']


class Tag(BaseModel):
    """
    标签
    """
    name = models.CharField('标签名', max_length=30, unique=True)

    def __str__(self):
        return self.name

    @property
    @utils.decorator_cache(60 * 60 * 5)  # 缓存5分钟
    def article_count(self):
        return Article.objects.filter(tag__name=self.name).distinct().count()

    class Meta:
        ordering = ['-created_time', 'name']


class Article(BaseModel):
    STATUS_CHOICES = (
        (1, '草稿'),
        (2, '发表')
    )

    STATUS_COMMENT = (
        (1, '打开'),
        (2, '关闭')
    )

    TYPE = (
        (1, '文章'),
        (2, '页面')
    )

    title = models.CharField(max_length=200, unique=True)
    body = models.TextField()
    pub_time = models.DateTimeField('发布时间', auto_now=True)
    status = models.SmallIntegerField('文章状态', choices=STATUS_CHOICES, default=1)
    status_comment = models.SmallIntegerField('评论状态', choices=STATUS_COMMENT, default=1)
    type = models.SmallIntegerField('类型', choices=TYPE, default=1)
    views = models.IntegerField('浏览次数', default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.SET_NULL,
                               blank=True, null=True)  # 使用 account 的 实体作为外键
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.SET_NULL, blank=True,
                                 null=True)  # 删除外键 设置为空
    tags = models.ManyToManyField(Tag, verbose_name='标签集合', through='ArticleTag')

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={
            'article_id': self.id,
            'year': self.created_time.year,
            'month': self.created_time.month,
            'day': self.created_time.day
        })

    def get_category_tree(self):
        tree = self.category.category_parent()
        names = list(map(lambda a: (a.name, a.get_absolute_url()), tree))
        return names


class ArticleTag(BaseModel):
    """
    建立这个类的目的是为了展示through 的用法， 这里面可以扩展多对多的额外关联数据(eg:created_time/modify_time)，
    同时也可以自定义on_delete的操作，因为多对多默认是级联删除
    """
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)  # 文章删除了 就把文章和标签的关系删除
    tag = models.ForeignKey(Tag, verbose_name='标签', on_delete=models.CASCADE)  # 标签删除了 就把文章和标签的关系删除


class Link(BaseModel):
    """
    友情链接
    """
    name = models.CharField('链接名称', max_length=30, unique=True)
    link = models.URLField('链接地址')
    sequence = models.IntegerField('排序', unique=True)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return self.name
