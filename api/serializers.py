from rest_framework import serializers
from spaces.models import Space, Tag, UserSpaceFollow
from posts.models import Post, Comment, CommentLikes, Reaction, ReactionType, SavedPosts
from authentication.models import UserFollows, Profile, UserReport
from django.contrib.auth import get_user_model

User = get_user_model()


class TagsSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ['id', 'slug', 'name']


class TagSerializer(serializers.ModelSerializer):
    space = TagsSpaceSerializer(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'space']


class UserSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'slug', 'username']

    def get_slug(self, obj):
        return obj.profile.slug


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class UserFollowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollows
        fields = ['following', 'follower']


class SpaceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, source='tag_set')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'image', 'user', 'followers_count', 'verified', 'created_at',
                  'updated_at', 'tags', 'slug']


class UserSpaceFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpaceFollow
        fields = ['id', 'user', 'space', 'created_at']

    def validate(self, data):
        if data['following'] == data['follower']:
            raise serializers.ValidationError("Потребител не може да се последва.")
        return data


class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReport
        fields = ['id', 'reporter', 'reported_user', 'report_type']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reactions = serializers.SerializerMethodField()
    space = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'space', 'tags', 'name', 'content', 'visibility', 'reactions', 'reactions_count',
                  'comments_count', 'images_count', 'rating', 'created_at', 'updated_at', 'slug']

    def get_reactions(self, obj):
        request = self.context.get('request')
        reaction_types = ReactionType.objects.all()

        if request and request.user.is_authenticated:
            user = request.user
            user_reactions = Reaction.objects.filter(user=user, post=obj).select_related('reaction_type')
            reacted_types = {reaction.reaction_type_id: True for reaction in user_reactions}
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

    def get_space(self, obj):
        space = getattr(obj, 'space', None)
        if space is not None:
            return {
                'slug': space.slug,
                'name': space.name,
                'verified': space.verified
            }
        else:
            return None


class SavedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPosts
        fields = ['user', 'post']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    show_replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'parent_comment', 'likes_count', 'is_liked', 'replies',
                  'show_replies', 'tagged_users', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_liked_by(request.user)
        return False

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all().order_by('-created_at'), many=True, context=self.context).data

    def get_show_replies(self, obj):
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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'visibility']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'instagram_handle', 'tiktok_handle', 'x_handle', 'facebook_url', 'bio', 'birth_date', 'gender',
                  'country', 'city']
