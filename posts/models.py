from django.contrib.auth.models import User
from django.db import models
from .validators import validate_len
from django.apps import apps


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey('spaces.Space', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, validators=[validate_len])
    content = models.TextField(validators=[validate_len])
    visibility = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def comments_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def reactions_count(self):
        return Reaction.objects.filter(post=self).count()

    @property
    def rating(self):
        weight_comments = 0.6
        weight_reactions = 0.4

        return (weight_comments * self.comments_count) + (weight_reactions * self.reactions_count)

    @property
    def tags(self):
        Tag = apps.get_model('spaces', 'Tag')
        return Tag.objects.filter(post=self)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    tagged_users = models.ManyToManyField(User, related_name='tagged_comments', blank=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def likes_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return CommentLikes.objects.filter(comment=self, user=user).exists()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.name} ({self.content})'


class CommentLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user.username} likes comment {self.comment.id}'


class ReactionType(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post', 'reaction_type')

    def __str__(self):
        return f'{self.user.username} reacted with {self.reaction_type.name} to {self.post.name}'
