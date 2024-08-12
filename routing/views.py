from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from posts.models import Post, Comment
from authentication.models import Profile
from spaces.models import Space


class Home(TemplateView):
    template_name = 'index.html'


class UserInfoEdit(TemplateView):
    template_name = 'user/info-edit.html'


class UserProfile(TemplateView):
    template_name = 'user/profile.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        profile = get_object_or_404(Profile, slug=slug)
        return profile.user

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        user = self.get_object()

        context['user'] = user

        context['is_owner'] = (user == self.request.user)

        context['posts'] = Post.objects.filter(user=user).order_by('-created_at')
        context['saved_posts'] = user.saved_posts.all()

        context['comments'] = Comment.objects.filter(user=user, parent_comment__isnull=True).order_by('-created_at')
        context['replies'] = Comment.objects.filter(user=user, parent_comment__isnull=False).order_by('-created_at')
        context['liked_comments'] = user.comment_likes.all()

        context['spaces'] = Space.objects.filter(user=user).order_by('-created_at')
        context['followed_spaces'] = user.followed_spaces.all()
        return context
