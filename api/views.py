from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from spaces.models import Space, Tag
from posts.models import Post, Comment
from .serializers import SpaceSerializer, TagSerializer, UserSpaceFollowSerializer, PostSerializer, CommentSerializer
from rest_framework import views
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from spaces.models import UserSpaceFollow


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
        return Response({"message": "Space followed successfully.", "data": f"{serializer}"}, status=status.HTTP_201_CREATED)


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
        return Response({"message": "Space unfollowed successfully."}, status=status.HTTP_201_CREATED)


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
    search_fields = ('name', )


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
    queryset = Comment.objects.filter()
    pagination_class = None

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_pk)
