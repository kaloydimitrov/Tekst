from django.contrib import admin
from .models import Post, ReactionType, Comment, CommentLikes, SavedPosts, PostImages

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ReactionType)
admin.site.register(CommentLikes)
admin.site.register(SavedPosts)
admin.site.register(PostImages)
