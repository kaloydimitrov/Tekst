from django.contrib import admin
from .models import Profile, UserFollows, UserReport

admin.site.register(Profile)
admin.site.register(UserFollows)
admin.site.register(UserReport)
