from rest_framework import serializers
from spaces.models import Space, Tag, UserSpaceFollow
from posts.models import Post, Comment, CommentLikes
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class SpaceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, source='tag_set')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'image', 'user', 'followers_count', 'created_at', 'updated_at', 'tags']


class UserSpaceFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpaceFollow
        fields = ['id', 'user', 'space', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'space', 'tags', 'name', 'content', 'visibility', 'views', 'comments_count', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'parent_comment', 'likes_count', 'is_liked', 'tagged_users', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLikes
        fields = ['user', 'comment']
