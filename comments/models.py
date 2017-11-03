from django.db import models
from django.conf import settings
from blog.models import Article


# Create your models here.
class BaseModel(models.Model):
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('最后修改时间', auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # TODO

    class Meta:
        abstract = True


class Comment(BaseModel):
    body = models.TextField('正文', max_length=300)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name="上级评论", blank=True, null=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return self.body

