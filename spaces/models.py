from django.contrib.auth.models import User
from django.db import models
from posts.models import Post
from .validators import validate_description_len, validate_name_len


class Space(models.Model):
    name = models.CharField(max_length=30, validators=[validate_name_len])
    description = models.TextField(validators=[validate_description_len])
    image = models.ImageField(upload_to='images/', blank=True, null=True)
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

    def __str__(self):
        return f"{self.name} (space: {self.space.name})"
