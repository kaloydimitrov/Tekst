from django.contrib import admin
from .models import Post, ReactionType, Comment

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ReactionType)
