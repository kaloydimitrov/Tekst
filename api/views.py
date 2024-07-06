from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from spaces.models import Space, Tag
from posts.models import Post, Comment, CommentLikes, Reaction
from .serializers import (SpaceSerializer, TagSerializer, UserSpaceFollowSerializer, PostSerializer, CommentSerializer,
                          CommentLikeSerializer, ReactionSerializer)
from rest_framework import views
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from spaces.models import UserSpaceFollow
from .permissions import IsOwner


# --------------------------------------
# SPACES
# --------------------------------------
class FollowSpaceView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        space = get_object_or_404(Space, pk=pk)
        user = request.user

        if UserSpaceFollow.objects.filter(user=user, space=space).exists():
            return Response({"detail": "Already following this space."}, status=status.HTTP_400_BAD_REQUEST)

        follow = UserSpaceFollow.objects.create(user=user, space=space)
        serializer = UserSpaceFollowSerializer(follow)
        return Response({"message": "Space followed successfully", "data": f"{serializer}"},
                        status=status.HTTP_201_CREATED)


class UnfollowSpaceView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, pk):
        space = get_object_or_404(Space, pk=pk)
        user = request.user

        follow = UserSpaceFollow.objects.filter(user=user, space=space).first()
        if not follow:
            return Response({"detail": "Not following this space."}, status=status.HTTP_400_BAD_REQUEST)

        follow.delete()
        return Response({"message": "Space unfollowed successfully"}, status=status.HTTP_201_CREATED)


class SpaceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description', 'user__username')


class SpaceDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer


class SpacePostsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        space_pk = self.kwargs['pk']
        return Post.objects.filter(space__pk=space_pk)


# --------------------------------------
# TAGS
# --------------------------------------
class TagListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)


# --------------------------------------
# COMMENTS
# --------------------------------------
class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        order = self.request.GET["order"]

        if order == 'oldest':
            return Comment.objects.filter(post_id=post_pk, parent_comment__isnull=True).order_by('created_at')
        elif order == 'top':
            return Comment.objects.filter(post_id=post_pk, parent_comment__isnull=True).annotate(total_likes=Count('likes')).order_by('-total_likes')

        return Comment.objects.filter(post_id=post_pk, parent_comment__isnull=True).order_by('-created_at')


class LikeCommentView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        user_id = request.user.pk
        like = CommentLikes.objects.filter(comment=pk, user=user_id)
        if like.exists():
            return Response({'error': 'You have already liked this comment'}, status=status.HTTP_400_BAD_REQUEST)

        like_serializer = CommentLikeSerializer(data={'comment': pk, 'user': user_id})
        if like_serializer.is_valid():
            like_serializer.save()
            return Response({'message': 'Comment liked'}, status=status.HTTP_201_CREATED)
        return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DislikeCommentView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, pk):
        comment = Comment.objects.get(pk=pk)
        user_likes = CommentLikes.objects.filter(comment=comment, user=request.user)
        if user_likes.exists():
            user_likes.delete()
            return Response({'message': 'Comment disliked'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'You have not liked this comment'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UpdateCommentView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# --------------------------------------
# REACTIONS
# --------------------------------------
class CreateReactionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReactionSerializer

    def perform_create(self, serializer):
        user = self.request.user
        post_id = serializer.validated_data['post'].id

        reaction = Reaction.objects.filter(user=user, post_id=post_id)
        if reaction.exists():
            reaction.delete()

        serializer.save(user=user)


class DeleteReactionView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post_id = request.data.get('post')
        reaction_type_id = request.data.get('reaction_type')

        try:
            reaction = Reaction.objects.get(user=request.user, post_id=post_id, reaction_type_id=reaction_type_id)
            reaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Reaction.DoesNotExist:
            return Response({'error': 'Reaction not found.'}, status=status.HTTP_404_NOT_FOUND)
