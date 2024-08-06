from django.urls import path, include
from routing.views import Home, UserInfo, UserPosts, UserComments

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('user/', include([
        path('info/', UserInfo.as_view(), name='user_info'),
        path('posts/', UserPosts.as_view(), name='user_posts'),
        path('comments/', UserComments.as_view(), name='user_comments'),
        # user_spaces
        # user_comments
    ]))
]
