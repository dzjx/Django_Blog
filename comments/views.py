from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from blog.models import Article
from comments.forms import CommentForm
from comments.models import Comment


class CommentPostView(generic.FormView):
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']

        article = Article.objects.get(pk=article_id)
        url = article.get_absolute_url()
        return HttpResponseRedirect(url + "#comments")

    def form_invalid(self, form):
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)
        u = self.request.user

        if self.request.user.is_authenticated:
            form.fields.update({
                'email': forms.CharField(widget=forms.HiddenInput()),
                'name': forms.CharField(widget=forms.HiddenInput()),
            })
            user = self.request.user
            form.fields["email"].initial = user.email
            form.fields["name"].initial = user.username

        return self.render_to_response({
            'form': form,
            'article': article
        })

    def form_valid(self, form):
        user = self.request.user
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)

        if not self.request.user.is_authenticated():
            email = form.cleaned_data['email']
            username = form.cleaned_data['name']

            user = get_user_model().objects.get_or_create(username=username, email=email)[0]

        comment = form.save(False)
        comment.article = article
        comment.author = user

        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(pk=form.cleaned_data['parent_comment_id'])
            comment.parent_comment = parent_comment

        comment.save(True)

        # 信号量
        from Django_Blog.blog_signals import comment_save_signal
        comment_save_signal.send(sender=self.__class__, comment_id=comment.id, username=user.username,
                                 server_port=self.request.get_port())

        return HttpResponseRedirect('{0}#div-comment-{1}'.format(article.get_absolute_url(), comment.pk))
