from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Notification
from authentication.models import UserFollows
from posts.models import Comment, Post
from spaces.models import Space


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


@receiver(post_save, sender=Comment)
def create_comment_notifications(sender, instance, created, **kwargs):
    if created:
        if instance.parent_comment:
            Notification.objects.create(
                notification_type='reply',
                user=instance.user,
                message=f"Ти отговори на коментар.",
                extra_data={
                    'comment_id': instance.parent_comment.id,
                    'post_slug': instance.post.slug
                },
            )

            Notification.objects.create(
                notification_type='reply',
                user=instance.parent_comment.user,
                message=f"{instance.user.username} отговори на твой коментар.",
                extra_data={
                    'comment_id': instance.parent_comment.id,
                    'post_slug': instance.post.slug
                },
            )
        else:
            comments_count = Comment.objects.filter(post=instance.post).count()
            if comments_count <= 10:
                post_author = instance.post.user
                if post_author and post_author != instance.user:
                    Notification.objects.create(
                        notification_type='reply',
                        user=post_author,
                        message=f"{instance.user.username} отговори на твоя публикация.",
                        extra_data={
                            'comment_id': instance.id,
                            'post_slug': instance.post.slug
                        }
                    )


@receiver(post_save, sender=Post)
def create_post_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            notification_type='post_created',
            user=instance.user,
            message=f"Създаде публикацията.",
            extra_data={
                'post_id': instance.id
            },
        )


@receiver(post_delete, sender=Post)
def create_post_deleted_notification(sender, instance, **kwargs):
    Notification.objects.create(
        notification_type='post_deleted',
        user=instance.user,
        message=f"Изтри публикация.",
    )


@receiver(post_save, sender=Space)
def create_space_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            notification_type='space_created',
            user=instance.user,
            message=f"Създаде тема.",
            extra_data={
                'space_id': instance.id,
                'space_name': instance.name
            },
        )


@receiver(post_delete, sender=Space)
def create_space_deleted_notification(sender, instance, **kwargs):
    Notification.objects.create(
        notification_type='space_deleted',
        user=instance.user,
        message=f"Изтри тема.",
        extra_data={
            'space_name': instance.name
        },
    )
