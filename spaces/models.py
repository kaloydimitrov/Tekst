from django.contrib.auth.models import User
from django.db import models
from posts.models import Post


class Space(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
