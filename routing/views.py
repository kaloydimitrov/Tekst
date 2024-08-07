from django.views.generic.base import TemplateView
from posts.models import Post, Comment


class Home(TemplateView):
    template_name = 'index.html'


class UserInfo(TemplateView):
    template_name = 'user/info.html'


class UserPosts(TemplateView):
    template_name = 'user/posts.html'

    def get_context_data(self, **kwargs):
        context = super(UserPosts, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.request.user)
        return context


class UserComments(TemplateView):
    template_name = 'user/comments.html'

    def get_context_data(self, **kwargs):
        context = super(UserComments, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(user=self.request.user, parent_comment__isnull=True)
        context['replies'] = Comment.objects.filter(user=self.request.user, parent_comment__isnull=False)
        return context
