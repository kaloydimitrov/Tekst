from django.contrib import admin
from .models import Post, ReactionType

admin.site.register(Post)
admin.site.register(ReactionType)
