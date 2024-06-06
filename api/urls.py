from django.urls import path
from django.urls import include
from .views import SpaceDetailView, SpaceListView, TagListView, FollowSpaceView, UnfollowSpaceView, SpacePostsView

urlpatterns = [
    path('space/', include([
        path('all/', SpaceListView.as_view(), name='get_all_spaces'),
        path('<int:pk>/', SpaceDetailView.as_view(), name='get_space_details'),
        path('<int:pk>/posts/', SpacePostsView.as_view(), name='get_space_posts'),
        path('follow/<int:pk>/', FollowSpaceView.as_view(), name='follow_space'),
        path('unfollow/<int:pk>/', UnfollowSpaceView.as_view(), name='unfollow_space')
    ])),
    path('tags/', include([
        path('all/', TagListView.as_view(), name='get_all_tags')
    ]))
]
