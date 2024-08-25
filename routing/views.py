from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from posts.models import Post, Comment
from spaces.models import Space
from authentication.models import Profile, UserFollows
from spaces.models import Space
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class Home(TemplateView):
    template_name = 'index.html'


def search(request):
    q = request.GET.get('q')

    if q:
        posts = Post.objects.filter(
            Q(name__icontains=q) | Q(content__icontains=q)
        )[:30]
        spaces = Space.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )[:30]
        users = User.objects.filter(
            Q(username__icontains=q)
        )[:30]
    else:
        posts = Post.objects.none()
        spaces = Space.objects.none()
        users = User.objects.none()

    context = {
        'q': q,
        'posts': posts,
        'spaces': spaces,
        'users': users
    }

    return render(request, 'search.html', context)


class UserInfoEdit(TemplateView):
    template_name = 'user/info-edit.html'


class UserProfile(TemplateView):
    template_name = 'user/profile.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        profile = get_object_or_404(Profile, slug=slug)
        user = profile.user
        message = None

        if profile.visibility == 'M' and profile.user != self.request.user:
            message = 'Профилът е скрит (само собственикът може да го види).'
        elif profile.visibility == 'F' and (not UserFollows.objects.filter(follower=self.request.user, following=profile.user).exists()) and profile.user != self.request.user:
            message = 'Само последователите и собственика могат да видят профила.'

        if message:
            return [user, message]

        return user

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        object_data = self.get_object()
        denied = False

        if isinstance(object_data, list):
            denied = True
            user = object_data[0]
            context['user'] = user
            context['denied_message'] = object_data[1]
        else:
            user = object_data
            context['user'] = user

        context['is_owner'] = (self.request.user == user)

        if UserFollows.objects.filter(follower=self.request.user, following=user).exists():
            context['followed'] = True
        else:
            context['followed'] = False

        context['followers_count'] = user.followers.count()
        context['following_count'] = user.following.count()

        if denied:
            return context

        if self.request.user == user:
            context['posts'] = Post.objects.filter(user=user).order_by('-created_at')
            context['saved_posts'] = user.saved_posts.all()
        else:
            context['posts'] = Post.objects.filter(user=user, visibility=True).order_by('-created_at')
            context['saved_posts'] = user.saved_posts.filter(post__visibility=True)

        context['comments'] = Comment.objects.filter(user=user, parent_comment__isnull=True).order_by('-created_at')
        context['replies'] = Comment.objects.filter(user=user, parent_comment__isnull=False).order_by('-created_at')
        context['liked_comments'] = user.comment_likes.all()

        context['spaces'] = Space.objects.filter(user=user).order_by('-created_at')
        context['followed_spaces'] = user.followed_spaces.all()

        context['display_choices'] = Profile.DISPLAY_CHOICES
        return context


class UserFollowersAndFollowing(TemplateView):
    template_name = 'user/followers-following.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = get_object_or_404(Profile, slug=slug)

        return profile.user

    def get_context_data(self, **kwargs):
        context = super(UserFollowersAndFollowing, self).get_context_data(**kwargs)
        user = self.get_object()

        context['user'] = user
        context['followers_list'] = user.followers.all()
        context['followings_list'] = user.following.all()

        return context
