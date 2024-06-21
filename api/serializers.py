from rest_framework import serializers
from spaces.models import Space, Tag, UserSpaceFollow
from posts.models import Post, Comment, CommentLikes, Reaction, ReactionType
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
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'space', 'tags', 'name', 'content', 'visibility', 'reactions', 'reactions_count', 'comments_count', 'rating', 'created_at', 'updated_at']

    def get_reactions(self, obj):
        request = self.context.get('request')
        user = request.user
        reaction_types = ReactionType.objects.all()
        user_reactions = Reaction.objects.filter(user=user, post=obj).select_related('reaction_type')
        reacted_types = {reaction.reaction_type_id: True for reaction in user_reactions}

        if request and request.user.is_authenticated:
            reactions = []
            for reaction_type in reaction_types:
                is_reacted = reacted_types.get(reaction_type.id, False)
                reactions.append({
                    'id': reaction_type.id,
                    'name': reaction_type.name,
                    'icon': reaction_type.icon,
                    'is_reacted': is_reacted
                })

            return reactions

        return [{'id': rt.id, 'name': rt.name, 'icon': rt.icon, 'is_reacted': False} for rt in reaction_types]


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


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['user', 'post', 'reaction_type']
        read_only_fields = ['user']
