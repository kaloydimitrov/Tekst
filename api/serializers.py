from rest_framework import serializers
from spaces.models import Space, Tag, UserSpaceFollow
from posts.models import Post
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

    class Meta:
        model = Post
        fields = ['id', 'user', 'space', 'name', 'content', 'visibility', 'views', 'created_at', 'updated_at']
