from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from authentication.models import UserFollows


@receiver(post_save, sender=UserFollows)
def create_follow_notifications(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            notification_type='follow',
            user=instance.following,
            message=f"{instance.follower.username} сега те следва.",
            extra_data={
                'username': instance.follower.username,
                'user_slug': instance.follower.profile.slug
            },
        )

        Notification.objects.create(
            notification_type='follow',
            user=instance.follower,
            message=f"Успешно последва {instance.following.username}.",
            extra_data={
                'username': instance.following.username,
                'user_slug': instance.following.profile.slug
            },
        )
