from django import template
from spaces.models import Space, UserSpaceFollow
from authentication.models import UserFollows
from django.db.models import Count
from notifications.models import Notification

register = template.Library()


@register.simple_tag
def get_verified_spaces():
    return Space.objects.filter(verified=True).order_by('-created_at')[:5]


@register.simple_tag
def get_top_spaces():
    return Space.objects.annotate(num_followers=Count('followers')).order_by('-num_followers')[:5]


@register.simple_tag
def get_followed_spaces(user):
    return UserSpaceFollow.objects.filter(user=user).order_by('-created_at')


@register.simple_tag
def get_followed_users(user):
    return UserFollows.objects.filter(follower=user)


@register.simple_tag
def get_notifications_count(user):
    return Notification.objects.filter(user=user, is_read=False).count()
