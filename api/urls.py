from django.urls import path
from django.urls import include
from .views import (SpaceDetailView, SpaceListView, TagListView, FollowSpaceView, UnfollowSpaceView, SpacePostsView,
                    CreateCommentView, CommentListView, LikeCommentView, DislikeCommentView, CreateReactionView,
                    DeleteReactionView, DeleteCommentView, UpdateCommentView, PostListView, CommentGetView,
                    PostSaveView, PostSavedRemoveView)

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
    ])),
    path('comment/', include([
        path('get/<int:pk>/', CommentGetView.as_view(), name='get_comment'),
        path('create/', CreateCommentView.as_view(), name='create_comment'),
        path('<int:post_pk>/', CommentListView.as_view(), name='get_post_comments'),
        path('<int:pk>/like/', LikeCommentView.as_view(), name='like_comment'),
        path('<int:pk>/dislike/', DislikeCommentView.as_view(), name='dislike_comment'),
        path('<int:pk>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
        path('<int:pk>/update/', UpdateCommentView.as_view(), name='update_comment')
    ])),
    path('reaction/', include([
        path('create/', CreateReactionView.as_view(), name='create_reaction'),
        path('delete/', DeleteReactionView.as_view(), name="delete_reaction")
    ])),
    path('post/', include([
        path('save/', PostSaveView.as_view(), name='save_post'),
        path('<int:pk>/remove-saved/', PostSavedRemoveView.as_view(), name='remove_saved_post'),
        path('all/', PostListView.as_view(), name='get_all_posts'),
    ]))
]
