from django.contrib import admin
from .models import Space, Tag, UserSpaceFollow

admin.site.register(Space)
admin.site.register(Tag)
admin.site.register(UserSpaceFollow)
