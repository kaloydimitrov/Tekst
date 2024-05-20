from django.contrib.auth.models import User
from django.db import models
from .validators import validate_len


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, validators=[validate_len])
    content = models.TextField(validators=[validate_len])
    visibility = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    tagged_users = models.ManyToManyField(User, related_name='tagged_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.name}'


class ReactionType(models.Model):
    name = models.CharField(max_length=50)

    # icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} reacted with {self.reaction_type.name} to {self.post.name}'
