from django.urls import path, include
from routing.views import Home, UserInfo, UserPosts

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('user/', include([
        path('info/', UserInfo.as_view(), name='user_settings'),
        path('posts/', UserPosts.as_view(), name='user_posts'),
        # user_spaces
        # user_comments
    ]))
]
